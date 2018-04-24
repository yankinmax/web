# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from html2text import html2text


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
    sentence_id = fields.Many2one(
        'task.results.sentences',
        string="Sentence",
        help="Will fill the results field with "
             "predefined sentence"
    )

    legal_reference = fields.Html(
        string="Legal reference",
        related="sale_line_id.product_tmpl_id.legal_reference",
        readonly=True,
    )

    conformity = fields.Selection(
        string="Task conformity",
        selection=[
            ("conform", "Compliant"),
            ("not_conform", "Not compliant"),
            ("warning", "Warning"),
        ],
        compute="_compute_conformity",
        readonly=False,
        store=True,
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

    def _test_parameters_check(self):
        if self.test_parameters:
            return all((self.test_parameters,
                        html2text(self.test_parameters).strip()))

    def _get_task_description(self):
        if self.description:
            return html2text(self.description)

    @api.depends("product_substance_measure_ids.conformity")
    def _compute_conformity(self):
        for record in self:
            conformities = record.mapped(
                "product_substance_measure_ids.conformity"
            )
            if "not_conform" in conformities:
                record.conformity = "not_conform"
            elif "warning" in conformities:
                record.conformity = "warning"
            else:
                record.conformity = "conform"

    @api.model
    def create(self, vals):
        rec = super(ProjectTask, self).create(vals)
        # sync w/ SO line
        rec.sync_with_so_line()
        return rec

    _so_line_prod_fields_to_sync = [
        'product_method_id',
        'equipment_id',
        'product_extraction_type_id',
        'test_parameters',
        'duration',
        'nb_shocks',
        'results',
    ]

    @api.multi
    def _get_values_from_so_line(self):
        """Retrieve task's value from `line` and `line.product_id`."""
        self.ensure_one()
        if not self.sale_line_id:
            return {}
        line = self.sale_line_id
        vals = {
            'tested_sample': line.tested_sample,
        }
        _values = line.product_id.read(
            self._so_line_prod_fields_to_sync, load='_classic_write')[0]
        del _values['id']
        for fname, val in _values.items():
            if val:
                vals[fname] = val
        return vals

    @api.multi
    def _get_task_measures_from_so_line(self):
        """Collect line's substance measures for given `task`."""
        self.ensure_one()
        if (not self.sale_line_id or
                not self.sale_line_id.product_substance_ids):
            return []
        task_measures = []
        for substance in self.sale_line_id.product_substance_ids:
            vals_measure = {
                'task_id': self.id,
                'product_substance_id': substance.id,
            }
            task_measures += [(0, 0, vals_measure)]
        return task_measures

    def _is_task_to_sync(self):
        """Check if we must sync task w/ SO line."""
        if self.env.context.get('so_sync_wizard'):
            # at this stage we have already everything in place
            # and we are forcing update via wizard.
            return True
        if not self.sale_line_id or self.product_substance_measure_ids:
            # no SO line or we already have substances...
            return False
        return (self.sale_line_id.state == 'sale' and
                self.sale_line_id._is_service_task())

    @api.multi
    def sync_with_so_line(self):
        """Sync values from SO line related to current tasks.

        The following conditions have to be satisfied for the sync:

        1. SO must be confirmed
        2. SO line must be tied to service products (`_is_procurement_task`)
        3. task already exists
        4. task has no substances yet (`task.product_substance_measure_ids`)

        What we sync:

        1. some values from the line itself (see `_get_values_from_so_line`)
        2. measures values attached to `line.product_substance_ids`
           (see `_get_task_measures_from_so_line`).

        You can skip this automatic update
        by setting `skip_task_sync` in the context.
        """
        if self.env.context.get('skip_task_sync'):
            return

        tasks = self.filtered(lambda x: x._is_task_to_sync())
        for task in tasks:
            task_values = task._get_values_from_so_line()
            if not task.product_substance_measure_ids:
                # No measure on task? Add them
                task_values['product_substance_measure_ids'] =  \
                    task._get_task_measures_from_so_line()
            task.with_context(skip_task_sync=True).write(task_values)

    @api.multi
    def button_toggle_substances_bdl(self):
        """Toggles the state of the whole BDL column.

        If all of checkboxes are checked - check them out.
        Otherwise - check them in.
        """
        self.ensure_one()
        bdl_values = self.product_substance_measure_ids.mapped('bdl')
        if all(bdl_values):
            self.product_substance_measure_ids.update({'bdl': False})
        else:
            self.product_substance_measure_ids.update({'bdl': True})

    @api.multi
    def button_toggle_substances_bql(self):
        """Toggles the state of the whole BQL column.

        If all of checkboxes are checked - check them out.
        Otherwise - check them in.
        """
        self.ensure_one()
        bql_values = self.product_substance_measure_ids.mapped('bql')
        if all(bql_values):
            self.product_substance_measure_ids.update({'bql': False})
        else:
            self.product_substance_measure_ids.update({'bql': True})
