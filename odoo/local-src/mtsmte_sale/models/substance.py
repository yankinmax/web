# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductSubstance(models.Model):
    _name = 'product.substance'

    name = fields.Char(
        string='Name',
        required=True,
    )
    legal_limit = fields.Float(
        string='Legal limit',
    )
    comments = fields.Char(
        string='Comments',
    )
    product_ids = fields.Many2many(
        'product.template',
        string='Products',
        required=True,
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Substance UOM',
        required=True,
    )
