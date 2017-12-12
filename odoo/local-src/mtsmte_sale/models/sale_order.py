# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
import html2text


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    analyze_sample = fields.Html(
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

    @api.multi
    @api.onchange('template_id')
    def onchange_template_id(self):
        """Quotation template changed

        When the quotation template is changed the sale order lines are
        updated accordingly but the substances linked to the product are not.

        So we need to link each line of the sale order to the corresponding
        substances of its product
        """
        super(SaleOrder, self).onchange_template_id()
        for record in self:
            for line in record.order_line:
                substances = line.product_id.product_substance_line_ids.mapped(
                    'product_substance_id')
                line.product_substance_ids = [(6, 0, substances.ids)]

    def _clean_html(self):
        clean_text = html2text.HTML2Text().handle(
            self.analyze_sample or ''
        ).strip()
        return clean_text

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for order in self:
            clean_text = order._clean_html()
            for line in order.order_line:
                if not line.tested_sample:
                    line.tested_sample = clean_text
        return res
