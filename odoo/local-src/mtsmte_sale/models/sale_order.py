# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    analyze_sample = fields.Text(
        string='Samples To Analyze',
    )
    commercial_partner_id = fields.Many2one(
        'res.partner',
        related='partner_id.commercial_partner_id',
        readonly=True,
    )

    @api.multi
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        for order in self:
            if not order.project_id:
                continue
            prj = self.env['project.project'].search(
                [('analytic_account_id', '=', order.project_id.id)])
            vals = {
                'analyze_sample': order.analyze_sample,
                'client_order_ref': order.client_order_ref,
            }
            prj.write(vals)
            for line in order.order_line:
                task = self.env['project.task'].search(
                    [('sale_line_id', '=', line.id)])
                # Adding measures todo in tasks
                product_substance_measure = []
                for substance in line.product_substance_ids:
                    vals_measure = {
                        'task_id': task.id,
                        'product_substance_id': substance.id,
                    }
                    product_substance_measure += [(0, 0, vals_measure)]
                task.write({
                    'product_substance_measure_ids': product_substance_measure,
                    'tested_sample': line.tested_sample,
                    'test_parameters': line.product_id.test_parameters,
                    'applied_dose': line.product_id.applied_dose,
                    'duration': line.product_id.duration,
                    'nb_shocks': line.product_id.nb_shocks,
                    'results': line.product_id.results,
                })
        return True
