# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models, fields


class AcountIvoice(models.Model):
    _inherit = 'account.invoice'

    report_numbers = fields.Char(
        string="Projects report numbers",
        compute="_compute_report_number",
        store=True,
    )

    @api.multi
    @api.depends('invoice_line_ids', 'invoice_line_ids.report_number')
    def _compute_report_number(self):
        for record in self:
            numbers = set(record.mapped('invoice_line_ids.report_number'))
            record.report_numbers = ', '.join(
                (val.strip() for val in numbers if val and val.strip())
            )


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
        compute="_compute_project_id",
    )
    report_number = fields.Char(
        string="Project report number",
        related="project_id.report_number",
    )

    @api.multi
    @api.depends('account_analytic_id',
                 'account_analytic_id.project_ids',
                 'account_analytic_id.project_ids.report_number')
    def _compute_project_id(self):
        for line in self:
            project = self.env['project.project'].search(
                [('analytic_account_id', '=', line.account_analytic_id.id)]
            )
            line.project_id = project
