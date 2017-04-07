# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    analyze_sample = fields.Text(
        string='Samples To Analyze',
    )

    @api.multi
    def action_confirm(self):
        Mesure = self.env['product.substance.measure']
        for order in self:
            super(SaleOrder, self).action_confirm()
            if order.project_id:
                prj = self.env['project.project'].search(
                    [('analytic_account_id', '=', order.project_id.id)])
                vals = {
                    'analyze_sample': order.analyze_sample
                }
                prj.write(vals)
                for line in order.order_line:
                    task = self.env['project.task'].search(
                        [('sale_line_id', '=', line.id)])
                    # Adding measures todo in tasks
                    vals_task = {'product_substance_measure_ids': []}
                    for substance in line.product_substance_ids:
                        vals_measure = {
                            'task_id': task.id,
                            'product_substance_id': substance.id,
                        }
                        measure = Mesure.create(vals_measure)
                        vals_task['product_substance_measure_ids'] += vals_measure
                    task.write(vals_task)
        return True
