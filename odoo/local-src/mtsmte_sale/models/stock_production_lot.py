# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    procurement_group_id = fields.Many2one(
        'procurement.group',
        string='Procurement Group',
    )
