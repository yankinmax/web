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
    new_expiry = fields.Date('New Expiry')
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
            # Propagate a manager to project
            if order.order_line:
                for sol in order.order_line:
                    # pick the first order line w/ `responsible_user_id`
                    # field set (if there are any) get the responsible for it's
                    # product_id (use responsible of product_id.categ_id as a
                    # fallback option), finally assign that guy to a project
                    if not (sol.product_id.responsible_user_id
                            or sol.product_id.categ_id.responsible_user_id):
                        continue
                    any_product = sol.product_id
                    responsible_user = any_product.responsible_user_id \
                        or any_product.categ_id.responsible_user_id
                    vals['user_id'] = responsible_user.id
                    break
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

        As well, this method propagates `tested_sample` field
        from `sale.quote.line` to `sale.order.line`s.
        """
        super(SaleOrder, self).onchange_template_id()
        # HACK: Here, we match freshly created `sale.order.line`s
        # w/ `sale.quote.line`s coming from a `template_id`.
        # NOTE: this approach is fine since the original method wipes out all
        # of the order lines and then repopulates those with templated lines,
        # so the order of those remains preserved.
        # And, of course, there is no way to inject that value carefully,
        # w/o using this kind of hacks or overriding the whole 64L method :)
        # IMO, the former is better.
        for record in self:
            for line, quote in zip(
                    record.order_line, record.template_id.quote_line):
                substances = line.product_id.product_substance_line_ids.mapped(
                    'product_substance_id')
                line.product_substance_ids = [(6, 0, substances.ids)]
                line.tested_sample = quote.tested_sample

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
                'tested_sample': html2text(vals['analyze_sample']),
            })
        return res

    @api.multi
    def action_sync_tasks(self):
        """Sync SO lines to tasks."""
        self.ensure_one()
        action = self.env.ref('mtsmte_sale.wiz_so_sync_task_action').read()[0]
        action['context'] = self.env.context.copy()
        return action
