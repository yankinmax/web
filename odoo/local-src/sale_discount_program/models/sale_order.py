# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    applied_program_ids = fields.Many2many(
        comodel_name='sale.discount.program',
    )

    @api.multi
    def apply_discount_programs(self):
        # TODO: Each program should reset itself ? (e.g. reset pricelist)
        # TODO: reset counter
        for line in self.mapped('order_line'):
            if line.source_program_id:
                line.unlink()

        programs = self.env['sale.discount.program'].search([])
        for sale in self:
            programs.apply_for_sale(sale)


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
