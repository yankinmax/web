# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    chemistry = fields.Selection(
        [('chem', 'Chemical Analysis'),
         ('test_env', 'Test Environment'),
         ('test_mec', 'Test Mécanique')],
    )
    product_substance_line_ids = fields.One2many(
        'product.substance.line',
        'product_id',
        string='Substance lines'
    )
    test_parameters = fields.Html(
        string='Test Parameters',
    )
    applied_dose = fields.Html(
        string='Applied Dose',
    )
    duration = fields.Html(
        string='Duration',
    )
    nb_shocks = fields.Html(
        string='Number of Shocks',
    )
    results = fields.Html(
        string='Results',
    )
    product_method_ids = fields.One2many(
        'product.method',
        'product_id',
        string='Methods',
    )
    equipment_ids = fields.One2many(
        'maintenance.equipment',
        'product_id',
        string='Equipment',
    )
    product_extraction_type_ids = fields.One2many(
        'product.extraction.type',
        'product_id',
        string='Extraction Type',
    )
