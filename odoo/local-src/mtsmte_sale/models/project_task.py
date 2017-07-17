# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_substance_measure_ids = fields.One2many(
        'product.substance.measure',
        'task_id',
        string='Substance Measure',
    )
    sale_line_id = fields.Many2one(index=True)
    tested_sample = fields.Text(
        string='Tested Samples',
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
        'task_id',
        string='Method',
    )
    equipment_ids = fields.One2many(
        'maintenance.equipment',
        'task_id',
        string='Equipment',
    )
    product_extraction_type_ids = fields.One2many(
        'product.extraction.type',
        'product_ids',
        string='Extraction Type',
    )
