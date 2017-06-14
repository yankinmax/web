# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    applied_program_ids = fields.Many2many(
        comodel_name='sale.discount.program',
        relation='sale_order_applied_program'
    )

    program_to_add = fields.Char(
        store=False
    )

    @api.onchange('program_to_add')
    def onchange_program_to_add(self):
        if self.program_to_add:
            values = {
                'program_to_add': False,
            }
            promo_code = self.env['sale.discount.program'].search([
                '|',
                ('promo_code', '=', self.program_to_add),
                ('voucher_code', '=', self.program_to_add),
            ], limit=1)
            if promo_code:
                if promo_code in self.program_code_ids:
                    ids = self.program_code_ids.ids
                    ids.remove(promo_code.id)
                    values['program_code_ids'] = [(6, False, ids)]
                else:
                    code_valid = (
                        promo_code.code_valid and
                        (
                            promo_code.promo_code or
                            promo_code.partner_id == self.partner_id
                        )
                    )
                    if code_valid:
                        ids = self.program_code_ids.ids + [promo_code.id]
                        values['program_code_ids'] = [(6, False, ids)]
            self.update(values)

    program_code_ids = fields.Many2many(
        comodel_name='sale.discount.program',
        domain=[
            '|', ('promo_code', '!=', False), ('voucher_code', '!=', False)
        ],
        string='Discount Codes'
    )

    program_code_ids_readonly = fields.Many2many(
        related='program_code_ids',
        store=False,
        readonly=True,
    )

    pricelist_program = fields.Boolean()

    supporting_document_required = fields.Boolean(
        compute='_compute_supporting_document_required',
    )
    supporting_document = fields.Binary(
        attachment=True
    )

    @api.depends('program_code_ids')
    def _compute_supporting_document_required(self):
        for order in self:
            order.supporting_document_required = any(
                program.sale_supporting_document_required
                for program in order.program_code_ids
            )

    @api.onchange('partner_id')
    def onchange_partner_id_remove_vouchers(self):
        """ Remove selected vouchers in sale.order when changing customer.
        """
        voucher_ids = self.program_code_ids.filtered(
            lambda p: p.voucher_code
        )
        if voucher_ids:
            self.order_line = self.order_line.filtered(
                lambda l: l.source_program_id not in voucher_ids
            )
            self.program_code_ids = self.program_code_ids.filtered(
                lambda p: not p.voucher_code
            )

    @api.onchange('pricelist_id')
    def onchange_pricelist_id(self):
        self.pricelist_program = False

    @api.multi
    def apply_discount_programs(self):
        self.ensure_one()
        if not self.order_line:
            raise UserError(
                _('You need to add order lines before apply discount')
            )
        program_model = self.env['sale.discount.program']
        program_model.reset_sale_programs(self)

        programs = program_model.sort_programs(
            self.program_code_ids | program_model.get_automatic_programs(self)
        )
        programs.apply_for_sale(self)

    @api.multi
    def force_apply(self):
        if self.env['ir.config_parameter'].get_param('force_discount_apply'):
            for sale in self.filtered(lambda s: s.state in ('draft', 'sent')):
                sale.apply_discount_programs()

    @api.multi
    def action_confirm(self):
        self.force_apply()

        for sale in self:
            sale.program_code_ids.sale_confirmed(sale.id)

        return super(SaleOrder, self).action_confirm()

    @api.multi
    def action_cancel(self):
        for sale in self:
            sale.program_code_ids.sale_cancelled(sale.id)

        return super(SaleOrder, self).action_cancel()

    @api.multi
    def action_quotation_send(self):
        self.force_apply()
        return super(SaleOrder, self).action_quotation_send()

    @api.multi
    def print_quotation(self):
        self.force_apply()
        return super(SaleOrder, self).print_quotation()

    @api.multi
    def check_current_month(self):
        self.ensure_one()
        today = fields.Date.from_string(
            fields.Date.today()
        )
        confirm_date = fields.Date.from_string(self.confirmation_date)
        return (
            confirm_date.year == today.year and
            confirm_date.month == today.month
        )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Which program create this line
    source_program_id = fields.Many2one(
        comodel_name='sale.discount.program',
    )

    # For which order line this program is
    source_order_line_id = fields.Many2one(
        comodel_name='sale.order.line'
    )

    discount_order_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='source_order_line_id'
    )

    # True if price_unit field was changed by a sale.discount.program
    price_program = fields.Boolean()

    # True if discount field was changed by a sale.discount.program
    discount_program = fields.Boolean()

    @api.onchange('discount')
    def onchange_discount(self):
        """ If discount is manually changed we don't reset it anymore.
        """
        self.discount_program = False

    @api.onchange(
        'product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id'
    )
    def _onchange_discount(self):
        """ Let sale computes pricelist discount, after we
        add a possible existing program discount on this line.
        """
        if self.discount_program:
            program_discount = self.discount
            self.discount = 0

        res = super(SaleOrderLine, self)._onchange_discount()

        if self.discount_program:
            self.discount += program_discount
        return res
