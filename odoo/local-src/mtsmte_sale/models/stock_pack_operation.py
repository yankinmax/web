# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class PackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    group_id = fields.Many2one(
        'procurement.group',
        readonly=True,
        related='picking_id.group_id'
    )
