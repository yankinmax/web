# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
try:
    from html2text import html2text
except ImportError:
    import logging
    _logger = logging.getLogger(__name__)
    _logger.warning('could not import html2text')


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
    # couldn't find a better way to fix this the error BSMTS-254
    # tests are fine
    project_project_id = fields.Many2one(
        store=True,
    )

    @api.multi
    def action_confirm(self):
        """Sync values on project."""
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

    def clean_analyze_sample(self):
        return html2text(self.analyze_sample or '')

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get('analyze_sample'):
            no_sample_lines = self.env['sale.order.line'].search(
                [('order_id', 'in', self.ids), ('tested_sample', '=', False)]
            )
            no_sample_lines.with_context(forced_write_from_order=True).write({
                'tested_sample': self._clean_html(vals['analyze_sample']),
            })
        return res
