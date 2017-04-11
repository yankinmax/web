# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_chemistry = fields.Boolean(
        string='Chemical analysis',
    )
    product_substance_ids = fields.Many2many(
        'product.substance',
        string='Substances',
    )
