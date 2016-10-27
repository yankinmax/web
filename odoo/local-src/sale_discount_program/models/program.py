# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import date

from openerp import _, api, fields, models
from openerp.exceptions import UserError
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class Program(models.Model):
    _name = 'sale.discount.program'

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
    max_use = fields.Integer(default=1)

    used = fields.Boolean(compute='_compute_used')

    voucher_amount = fields.Float(
        compute='_compute_voucher_amount',
        inverse='_inverse_voucher_amount',
        store=True,
    )

    code_valid = fields.Boolean(compute='_compute_code_valid', store=True)

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
            return self.env['ir.sequence'].next_by_code(
                'discount.program.voucher_code'
            )
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

    @api.depends('program_name', 'promo_code', 'voucher_code')
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

    def _inverse_voucher_amount(self):
        for program in self:
            if program.voucher_amount:
                product_add_price = -1 * program.voucher_amount
                if program.action_ids:
                    program.action_ids.unlink()

                program.write({
                    "action_ids": [(0, False, {
                        'type_action': 'product_add',
                        'product_add_id': self.env.ref(
                            'sale_discount_program.product_voucher'
                        ).id,
                        'product_add_force_price': True,
                        'product_add_price': product_add_price,
                        'allow_negative_total': False,
                    })]
                })

    @api.depends('expiration_date', 'nb_use', 'max_use')
    def _compute_code_valid(self):
        for program in self:
            code_valid = True
            if program.automatic:
                code_valid = False
            else:
                if program.expiration_date:
                    today = date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
                    if program.expiration_date < today:
                        code_valid = False

                if program.max_use and program.nb_use >= program.max_use:
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

        # TODO: and / or
        return any(condition.check(sale) for condition in self.condition_ids)

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
        if self.voucher_code:
            not_combinable = not_combinable.filtered(
                lambda p: p.voucher_code
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
    def sale_confirmed(self):
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

    def sale_cancelled(self):
        """ Called when a sale.order is cancelled if this program is applied
        on the sale.order.
        """
        for program in self:
            if not program.automatic:
                program.sudo().nb_use -= 1

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

    @api.model
    def get_automatic_programs(self):
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
