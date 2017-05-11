# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _compute_tax_id(self):
        for line in self:
            order = line.order_id
            invoice = self.env['account.invoice'].new({
                'partner_id': order.partner_id.id,
                'type': 'out_invoice',
                'fiscal_position_id': order.fiscal_position_id.id,
                'company_id': order.company_id.id,
            })
            invoice_line = self.env['account.invoice.line'].new({
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'invoice_id': invoice.id,
            })
            invoice_line._onchange_product_id()
            line.tax_id = invoice_line.invoice_line_tax_ids.ids
