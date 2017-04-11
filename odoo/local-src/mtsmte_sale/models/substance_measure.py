# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductSubstanceMesure(models.Model):
    _name = 'product.substance.measure'
    _rec_name = "product_substance_id"

    product_substance_id = fields.Many2one(
        'product.substance',
        string='Substance',
        required=True,
    )
    task_id = fields.Many2one(
        'project.task',
        string='Task',
        required=True,
    )
    measure = fields.Float(
        'Measure',
    )
    conformity = fields.Boolean(
        string='Conformity',
    )
    legal_limit = fields.Float(
        string='Legal limit',
        related="product_substance_id.legal_limit",
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Substance UOM',
        required=True,
        related="product_substance_id.product_uom_id",
    )
