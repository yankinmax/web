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
    def write(self, vals):
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

        so, here we fix this to proper m2m write values.

        See https://github.com/odoo/odoo/issues/19239
        """
        for so_line in vals.get('order_line', []):
            if so_line[0] == 0 and so_line[-1].get('product_substance_ids'):
                so_line[-1]['product_substance_ids'] = [
                    (6, 0, [x[1]
                            for x in so_line[-1]['product_substance_ids']])
                ]
        return super(SaleOrder, self).write(vals)

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

                vals = {
                    'product_substance_measure_ids': product_substance_measure,
                    'tested_sample': line.tested_sample,
                    'test_parameters': line.product_id.test_parameters,
                    'applied_dose': line.product_id.applied_dose,
                    'duration': line.product_id.duration,
                    'nb_shocks': line.product_id.nb_shocks,
                    'results': line.product_id.results,
                }

                product_method_id = line.product_id.product_method_id.id
                equipment_id = line.product_id.equipment_id.id
                extraction_id = line.product_id.product_extraction_type_id.id

                if product_method_id:
                    vals['product_method_id'] = product_method_id
                if equipment_id:
                    vals['equipment_id'] = equipment_id
                if extraction_id:
                    vals['product_extraction_type_id'] = extraction_id
                task.write(vals)

        return True
