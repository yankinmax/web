# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    applied_program_ids = fields.Many2many(
        comodel_name='sale.discount.program',
        relation='sale_order_applied_program'
    )

    program_code_ids = fields.Many2many(
        comodel_name='sale.discount.program',
        domain=[
            '|', ('promo_code', '!=', False), ('voucher_code', '!=', False)
        ],
        string='Discount Codes'
    )

    pricelist_program = fields.Boolean()

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
            self.program_code_ids | program_model.get_automatic_programs()
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
            sale.program_code_ids.sale_confirmed()

        return super(SaleOrder, self).action_confirm()

    @api.multi
    def action_cancel(self):
        for sale in self:
            sale.program_code_ids.sale_cancelled()

        return super(SaleOrder, self).action_cancel()

    @api.multi
    def action_quotation_send(self):
        self.force_apply()
        return super(SaleOrder, self).action_quotation_send()

    @api.multi
    def print_quotation(self):
        self.force_apply()
        return super(SaleOrder, self).print_quotation()


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

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        """ Let product_visible_discount computes pricelist discount, after we
        add a possible existing program discount on this line.
        """
        if self.discount_program:
            program_discount = self.discount
            self.discount = 0

        res = super(SaleOrderLine, self).product_uom_change()

        if self.discount_program:
            self.discount += program_discount
        return res
