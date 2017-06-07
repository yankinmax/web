# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from html2text import html2text


class Helpers(models.AbstractModel):
    _name = 'report.mtsmte_reports.report_project_analysis'

    mech_test_fields = (
        'applied_dose',
        'duration',
        'nb_shocks',
    )

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report_name = self._name.split('report.')[-1]
        report = report_obj._get_report_from_name(report_name)
        if docids:
            docs = self.env[report.model].browse(docids)
            tasks = []
        else:
            docs = self.env[report.model].browse(data['project_id'])
            tasks = self.env['project.task'].browse(data['task_ids'])
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'tasks': tasks,
            'report': self,
            'forced_lang': data.get('lang'),
        }
        return report_obj.render(report_name, docargs)

    def get_analysis_type(self, product):
        return 'chemical' if product.chemistry == 'chem' else 'mech_env'

    def task_field_info(self, fname):
        return self.env['project.task'].fields_get(
            allfields=[fname, ])[fname]

    def get_mech_env_details(self, task):
        details = {}
        for fname in self.mech_test_fields:
            # an "empty" field contains u'<p><br></p>'
            if html2text(task[fname]).strip():
                info = self.task_field_info(fname)
                details['label'] = info['string']
                details['val'] = task[fname]
        return details
