# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_substance_ids = fields.Many2many(
        'product.substance',
        string='Substances',
    )
    chemistry = fields.Selection(
        related='product_id.chemistry',
        readonly=True,
    )
    tested_sample = fields.Text(
        string='Tested Samples',
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.product_substance_ids = self.product_id.product_substance_ids
