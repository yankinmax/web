# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_substance_ids = fields.Many2many(
        'product.substance',
        string='Substances',
    )
    chemistry = fields.Selection(
        related='product_id.chemistry',
        readonly=True,
    )
    tested_sample = fields.Text(
        string='Tested Samples',
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        for line in self.product_id.product_substance_line_ids:
            self.product_substance_ids |= line.product_substance_id

    def _fix_substances_values(self, vals):
        """Fix for `product_substance_ids` m2m BSMTS-140.

        We set the field value w/ an onchange in SO line.
        When you create a new line you save the order
        the value is converted to something like:

        u'product_substance_ids': [
            #  _, SUB ID, _
            [1, 1, {u'product_uom_id': 20}],
            [1, 4, {u'product_uom_id': 20}],
            [1, 7, {u'product_uom_id': 20}],
        ]

        or we can have pure ids w/out any command like:

            [1, 4, 7]

        so, here we fix this to proper m2m write values.

        See https://github.com/odoo/odoo/issues/19239
        """
        sub_ids = vals.get('product_substance_ids', [])
        if not sub_ids:
            return
        # if you add value manually instead of onchange
        # you get the correct form: [6, False, [9, 1, 4, 7]]
        fixed = []
        got_pure_ids = all([isinstance(x, int) for x in sub_ids])
        if got_pure_ids:
            # we got a list of ids [9, 4, 7]
            fixed = [(6, 0, sub_ids)]
        else:
            # merge all values here and pass only one command at the end
            all_ids = []
            for x in sub_ids:
                if x[0] == 6:
                    all_ids.extend(x[-1])
                elif x[0] != 6 and len(x) > 1 and not x[1] in all_ids:
                    # include missing ones w/ bad form
                    all_ids.append(x[1])
            fixed = [(6, 0, all_ids)]
        if fixed:
            vals['product_substance_ids'] = fixed

    @api.model
    def create(self, vals):
        self._fix_substances_values(vals)
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    def write(self, vals):
        self._fix_substances_values(vals)
        res = super(SaleOrderLine, self).write(vals)
        if vals.get('product_substance_ids'):
            # Updating substances on the line -> update task
            self.update_task_values()
        return res

    @api.multi
    def _action_procurement_create(self):
        """Update SO line related project tasks after tasks creation.

        When a SO is confirmed,
        `procurement` machinery creates one procurement for each SO line.

        `sale_timesheet.models.procurement.ProcurementOrder` overrides `_run`
        to create "service tasks", for lines that relate service products
        (see `_is_procurement_task` below).

        This behavior is further extended by
        `sale_project_fixed_price_task_completed_invoicing`.

        Here we hook to make sure
        that we update tasks right after their creation.
        """
        procs = super(SaleOrderLine, self)._action_procurement_create()
        # now we have tasks to update
        self.update_task_values()
        return procs

    @api.multi
    def get_line_task(self):
        self.ensure_one()
        return self.env['project.task'].search([
            ('sale_line_id', '=', self.id)
        ])

    _prod_fields_to_sync = [
        'product_method_id',
        'equipment_id',
        'product_extraction_type_id',
        'test_parameters',
        'duration',
        'nb_shocks',
        'results',
    ]

    @api.multi
    def _get_task_values(self):
        """Retrieve task's value from `line` and `line.product_id`."""
        self.ensure_one()
        vals = {
            'tested_sample': self.tested_sample,
        }
        _values = self.product_id.read(
            self._prod_fields_to_sync, load='_classic_write')[0]
        del _values['id']
        for fname, val in _values.items():
            if val:
                vals[fname] = val
        return vals

    @api.multi
    def _get_task_measures_values(self, task):
        """Collect line's substance measures for given `task`."""
        task_measures = []
        for substance in self.product_substance_ids:
            vals_measure = {
                'task_id': task.id,
                'product_substance_id': substance.id,
            }
            task_measures += [(0, 0, vals_measure)]
        return task_measures

    def _is_procurement_task(self):
        # same conditions as
        # sale-workflow/sale_project_fixed_price_task_completed_invoicing/models/procurement.py  # noqa
        return (self.product_id.type == 'service' and
                self.product_id.track_service in ('task', 'completed_task'))

    @api.multi
    def update_task_values(self):
        """Sync values on project tasks related to current lines.

        The following conditions have to be satisfied for the sync:

        1. SO must be confirmed
        2. SO line must be tied to service products (`_is_procurement_task`)
        3. task already exists
        4. task has no substances yet (`task.product_substance_measure_ids`)

        What we sync:

        1. some values from the line itself (see `_get_task_values`)
        2. measures values attached to `line.product_substance_ids`
           (see `_get_task_measures_values`).

        You can skip this automatic update
        by setting `skip_task_sync` in the context.
        """
        if self.env.context.get('skip_task_sync'):
            return
        lines = self.filtered(lambda x: x.order_id.state == 'sale'
                              and x._is_procurement_task())
        for line in lines:
            task = line.get_line_task()
            if not task:
                # no task, nothing to do
                continue
            task_values = line._get_task_values()
            if not task.product_substance_measure_ids:
                # No measure on task? Add them
                task_values['product_substance_measure_ids'] =  \
                    line._get_task_measures_values(task)
            task.write(task_values)
