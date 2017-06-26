# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import shortuuid

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Program(models.Model):
    _name = 'sale.discount.program'
    _inherit = 'mail.thread'

    name = fields.Char('Name', compute='_compute_name', store=True)

    program_name = fields.Char()

    automatic = fields.Boolean(
        compute='_compute_automatic',
        store=True,
        default=True,
    )

    combinable = fields.Boolean(default=True)

    promo_code = fields.Char('Promo code')
    voucher_code = fields.Char(
        'Voucher code', default=lambda self: self._default_voucher_code()
    )

    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')

    expiration_date = fields.Date()
    nb_use = fields.Integer()

    confirmed_sales_which_used = fields.Many2many(
        comodel_name='sale.order',
        relation='sale_discount_program_confirmed_sale_order_which_used_rel',
        string='Confirmed sales which used',
        readonly=True,
    )
    max_use = fields.Integer(default=1)
    max_use_by_month = fields.Integer(default=1)

    used = fields.Boolean(compute='_compute_used')

    sale_supporting_document_required = fields.Boolean()

    voucher_amount = fields.Float(
        compute='_compute_voucher_amount',
        inverse='_inverse_voucher_amount',
        store=True,
    )

    code_valid = fields.Boolean(compute='_compute_code_valid', store=True)

    conditions_and = fields.Boolean(
        string="All conditions must match",
        help="If checked, all conditions should match for apply this program. "
             "Otherwise one matching condition is enough "
             "for apply this program."
    )

    condition_ids = fields.One2many(
        comodel_name='sale.discount.program.condition',
        inverse_name='program_id',
        string='Conditions',
    )

    action_ids = fields.One2many(
        comodel_name='sale.discount.program.action',
        inverse_name='program_id',
        string='Actions',
    )

    _sql_constraints = [
        ('uniq_voucher_code',
         'unique(voucher_code)',
         _("Voucher code should be unique")),
        ('uniq_promo_code',
         'unique(promo_code)',
         _("Promo code should be unique"))
    ]

    def _default_voucher_code(self):
        if self.env.context.get('program_voucher'):
            return shortuuid.uuid()[:10]
        else:
            return False

    @api.depends(
        'program_name', 'voucher_code', 'promo_code', 'voucher_amount'
    )
    def _compute_name(self):
        for program in self:
            if program.promo_code:
                program.name = "%s: %s" % (_("Promo code"), program.promo_code)

            elif program.voucher_code:
                program.name = "%s: %s (%s)" % (
                    _("Voucher"),
                    program.voucher_code,
                    program.voucher_amount
                )

            else:
                program.name = program.program_name

    @api.depends('promo_code', 'voucher_code')
    def _compute_automatic(self):
        for program in self:
            program.automatic = not bool(
                program.promo_code or program.voucher_code
            )

    @api.depends('action_ids', 'action_ids.product_add_price')
    def _compute_voucher_amount(self):
        for program in self:
            if program.action_ids and program.action_ids[0].product_add_price:
                program.voucher_amount = (
                    -1 * program.action_ids[0].product_add_price
                )
            else:
                program.voucher_amount = False

    def _get_action_values_for_voucher_amount(self, product_add_price):
        return {
            'type_action': 'product_add',
            'product_add_id': self.env.ref(
                'sale_discount_program.product_voucher'
            ).id,
            'product_add_force_price': True,
            'product_add_price': product_add_price,
            'allow_negative_total': False,
        }

    def _inverse_voucher_amount(self):
        for program in self:
            if program.voucher_amount:
                # Let the get product_add_price value here,
                # because unlink will be drop it
                product_add_price = -1 * program.voucher_amount
                if program.action_ids:
                    program.action_ids.unlink()

                action_values = program._get_action_values_for_voucher_amount(
                    product_add_price
                )
                program.write({
                    "action_ids": [
                        (0, False, action_values)
                    ]
                })

    @api.depends('expiration_date', 'nb_use', 'max_use', 'max_use_by_month')
    def _compute_code_valid(self):
        today = fields.Date.today()
        for program in self:
            code_valid = True
            if program.automatic:
                code_valid = False
            else:
                if program.expiration_date:
                    if program.expiration_date < today:
                        code_valid = False

                if program.max_use and program.nb_use >= program.max_use:
                    code_valid = False

            confirmed_sales_which_used = (
                program.sudo().confirmed_sales_which_used
            )
            check_max_use_by_month = (
                code_valid and
                program.max_use_by_month and
                confirmed_sales_which_used
            )
            if check_max_use_by_month:
                current_confirmed_sales_which_used = (
                    confirmed_sales_which_used.filtered(
                        lambda s: s.check_current_month()
                    )
                )
                sale_count = len(current_confirmed_sales_which_used)
                if sale_count >= program.max_use_by_month:
                    code_valid = False

            program.code_valid = code_valid

    @api.depends('nb_use', 'max_use')
    def _compute_used(self):
        for program in self:
            program.used = program.nb_use >= program.max_use

    @api.multi
    def is_applicable(self, sale):
        self.ensure_one()

        if not self.check_combinable(sale):
            return False

        if not self.automatic:
            if not self.code_valid:
                raise UserError(_("%s is not valid anymore.") % self.name)

            if self.voucher_amount:
                self.check_voucher_limits(sale)

            return True

        else:
            if not self.condition_ids:
                return True

        if self.conditions_and:
            match = all(
                condition.check(sale) for condition in self.condition_ids
            )
        else:
            match = any(
                condition.check(sale) for condition in self.condition_ids
            )
        return match

    @api.multi
    def check_voucher_limits(self, sale):
        """ Check if already applied voucher is not bigger than quotation total
        """
        if sale.amount_total <= 0:
            raise UserError(_(
                'Too many vouchers for the quotation amount'
            ))

    def check_combinable(self, sale):
        """ Check if already applied programs are not marked as not combinable.
        """
        # TODO: Find a better way to manage combination limit of programs ?
        self.ensure_one()

        not_combinable = sale.applied_program_ids.filtered(
            lambda p: not p.combinable
        )
        if not_combinable:
            if self.automatic:
                return False
            else:
                raise UserError(_(
                    '%s can not be combined with %s .'
                    'Please remove it and apply discounts again.'
                    % (self.name, ", ".join(not_combinable.mapped('name')))
                ))
        else:
            return True

    def set_applied(self, sale):
        self.ensure_one()
        sale.write({'applied_program_ids': [(4, self.id)]})

    @api.multi
    def apply_actions(self, sale):
        """ Apply all actions of this program on sale.order *sale*.
        """
        self.ensure_one()
        for action in self.action_ids:
            action.apply(sale)
        self.set_applied(sale)

    @api.multi
    def apply_for_sale(self, sale, raise_no_discount=False):
        """ Apply this action on sale.order *sale*.
        """
        for program in self:
            if program.is_applicable(sale):
                program.apply_actions(sale)

    @api.multi
    def sale_confirmed(self, sale_id):
        """ Called when a sale.order is confirmed if this program is applied
        on the sale.order.
        """
        for program in self:
            if not program.automatic:
                if not program.code_valid:
                    raise UserError(
                        _("%s is not valid anymore.") % program.name
                    )

                program.sudo().nb_use += 1
                program.sudo().write({
                    'confirmed_sales_which_used': [(4, sale_id, False)]
                })

    def sale_cancelled(self, sale_id):
        """ Called when a sale.order is cancelled if this program is applied
        on the sale.order.
        """
        for program in self:
            if not program.automatic:
                program.sudo().nb_use -= 1
                program.sudo().write({
                    'confirmed_sales_which_used': [(3, sale_id, False)]
                })

    @api.model
    def reset_sale_programs(self, sale):
        """ Cancel all programs modification for this *sale*
        """
        sale.ensure_one()
        sale.write({'applied_program_ids': [(5,)]})
        for line in sale.order_line:
            if line.source_program_id:
                line.unlink()
            elif line.discount_program:
                line.write({
                    'discount': False,
                    'discount_program': False
                })

        if sale.pricelist_program:
            sale.pricelist_id = sale.partner_id.property_product_pricelist
            for line in sale.order_line:
                line.product_uom_change()
                line._onchange_discount()

    @api.model
    def get_automatic_programs(self, order):
        """ Return all programs marked as automatic.
        """
        return self.search([
            ('automatic', '=', True)
        ])

    @api.model
    def sort_programs(self, programs):
        """ Method to sort a program recordset *programs* before try to apply
        them. Main goal of this method is to be easily override,
        """
        return programs.sorted(lambda p: (p.combinable, p.id))
