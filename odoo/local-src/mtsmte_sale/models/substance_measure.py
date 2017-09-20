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
        string='Measure',
        help='The value 0 is considered as NULL',
    )
    conformity = fields.Selection(
        string='Conformity',
        selection=[('conform', 'Conform'),
                   ('warning', 'Warning'),
                   ('not_conform', 'Not conform')],
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
    bdl = fields.Boolean(
        string='DBL',
        related='task_id.bdl',
        readonly=True
    )

    @staticmethod
    def less(value1, value2):
        return float_compare(value1, value2, precision_digits=2) < 0

    def measure_in_limits(self):
        self.ensure_one()
        return all((self.less(self.legal_limit_min, self.measure),
                    self.less(self.measure, self.legal_limit_max)))

    def has_limits(self, kind):
        self.ensure_one()
        if kind == 'all':
            return all((self.has_limit_min, self.has_limit_max))
        elif kind == 'any':
            return any((self.has_limit_min, self.has_limit_max))
        else:
            raise TypeError("Wrong kind for a limits check")

    def _compute_conformity_conform(self):
        return (self.bdl
                or (not self.has_limits('all')
                    and self.measure_in_limits())
                or (self.has_limits('any')
                    and self.measure_in_limits()))

    def _compute_conformity_warning(self):
        return (not self.has_limits('any')
                and not self.measure_in_limits())

    def _compute_conformity_not_conform(self):
        return (self.has_limits('any')
                and not self.measure_in_limits())

    @api.depends('legal_limit_min',
                 'has_limit_min',
                 'legal_limit_max',
                 'has_limit_max',
                 'measure',
                 'bdl')
    def _compute_conformity(self):
        for record in self:
            if record._compute_conformity_conform():
                record.conformity = 'conform'
            elif record._compute_conformity_warning():
                record.conformity = 'warning'
            elif record._compute_conformity_not_conform():
                record.conformity = 'not_conform'
