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
            order.order_line.set_measures()
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
            if 'order_line' in vals:
                order.order_line.set_measures()
            clean_text = order._clean_html()
            for line in order.order_line:
                if not line.tested_sample:
                    line.tested_sample = clean_text
        return res
