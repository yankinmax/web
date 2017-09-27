# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


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
    product_method_id = fields.Many2one(
        'product.method',
        string='Method',
    )
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipment',
    )
    product_extraction_type_id = fields.Many2one(
        'product.extraction.type',
        string='Extraction Type',
    )
    bdl = fields.Boolean(
        string='BDL',
        help='When selected, all measures are considered Conform'
    )
    sentence_id = fields.Many2one(
        'task.results.sentences',
        string="Sentence",
        help="Will fill the results field with "
             "predefined sentence"
    )

    @api.onchange("sentence_id")
    def _onchange_sentence_id(self):
        # There is a bug with Html fields. If you delete its content
        # via ctrl+a backspace or selecting all the data and backspace
        # it won't actually trigger html field onchange and will return
        # its old value. Doesn't happen when you delete content symbol-
        # by-symbol via backspacing. So beware not to explode on that
        for record in self:
            record.results = record.sentence_id.sentence
