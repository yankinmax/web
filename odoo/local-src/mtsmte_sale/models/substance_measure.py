# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.tools import float_compare


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
        compute='_compute_conformity',
        readonly=True,
    )
    legal_limit_min = fields.Float(
        string='Legal limit min value',
        related="product_substance_id.legal_limit_min",
        readonly=True,
    )
    has_limit_min = fields.Boolean(
        string='Has limit min',
        related="product_substance_id.has_limit_min",
        readonly=True,
    )
    has_limit_max = fields.Boolean(
        string='Has limit max',
        related="product_substance_id.has_limit_max",
        readonly=True,
    )
    legal_limit_max = fields.Float(
        string='Legal limit max value',
        related="product_substance_id.legal_limit_max",
        readonly=True,
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Substance UOM',
        required=True,
        related="product_substance_id.product_uom_id",
        readonly=True,
    )
    detection_limit = fields.Char(
        string='Detection Limit',
        related='product_substance_id.detection_limit',
        readonly=True,
    )
    quantification_limit = fields.Char(
        string='Quantification Limit',
        related='product_substance_id.quantification_limit',
        readonly=True,
    )
    sub_cas_number = fields.Char(
        string='CAS Number',
        related='product_substance_id.sub_cas_number',
        readonly=True,
    )
    comments = fields.Char(
        string='Comments',
        related='product_substance_id.comments',
        readonly=True,
    )

    @api.depends('legal_limit_min', 'legal_limit_max', 'measure')
    def _compute_conformity(self):
        for record in self:
            conformity = True
            if (record.has_limit_max and
                    (float_compare(record.measure, record.legal_limit_max,
                                   precision_digits=2)) > 0):
                conformity = False
            if (record.has_limit_min and
                    (float_compare(record.legal_limit_min, record.measure,
                                   precision_digits=2)) > 0):
                conformity = False
            record.conformity = conformity
