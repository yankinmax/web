# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductSubstanceLine(models.Model):
    _name = 'product.substance.line'
    _rec_name = 'product_substance_id'

    product_substance_id = fields.Many2one(
        'product.substance',
        string='Substance',
        required=True,
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
    comments = fields.Char(
        string='Comments',
        related="product_substance_id.comments",
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
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        domain=[('customer', '=', True)],
        readonly=True,
    )
    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True,
    )
    sub_cas_number_ids = fields.One2many(
        'substance.cas.number',
        'substance_id',
        string='CAS Number',
        related='product_substance_id.sub_cas_number_ids',
        readonly=True,
    )
