# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProjectAnalyisPrintWiz(models.TransientModel):
    _name = 'project.analysis.print.wiz'

    project_id = fields.Many2one(
        string='Project',
        comodel_name='project.project',
        required=True,
    )
    lang_id = fields.Many2one(
        string='Language',
        comodel_name='res.lang',
        required=True,
        default=lambda self: self._default_lang_id(),
    )
    task_ids = fields.Many2many(
        string='Tasks',
        comodel_name='project.task',
        domain=lambda self: self._domain_task_ids(),
        default=lambda self: self._default_task_ids(),
    )

    def _default_lang_id(self):
        lang = self.project_id.partner_id.lang
        if not lang:
            lang = self.env.context.get('lang', 'en_US')
        return self.env['res.lang'].search([('code', '=', lang)], limit=1)

    def _domain_task_ids(self):
        return [('project_id', '=', self.env.context.get('active_id'))]

    def _default_task_ids(self):
        return self.env['project.task'].search(self._domain_task_ids())

    @api.multi
    def print_it(self):
        self.ensure_one()
        report = self.env.ref('mtsmte_reports.action_report_analysis')
        res = report.read()[0]
        to_keep = (
            'model', 'type',
            'report_name', 'report_type', 'name'
        )
        res = {k: v for k, v in res.iteritems() if k in to_keep}
        res['data'] = {
            'lang': self.lang_id.code,
            'project_id': self.project_id.id,
            'task_ids': self.task_ids.ids,
        }
        return res
