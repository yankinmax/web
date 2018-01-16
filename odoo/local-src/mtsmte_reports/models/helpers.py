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

    def _get_conformity_options(self, lang):
        """Returns translated options for conformity

        Due to mysterious reasons conformity selection was not
        getting translated in the project analysis report. After
        headbanging it with Simone for sometime it was decided to
        hack it through the roof.
        :param lang: language to translate the field to
        :returns: dictionary with translated values
        """
        model = self.env["product.substance.measure"].with_context(lang=lang)
        return dict(
            model.fields_get(['conformity'])['conformity']['selection']
        )

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report_name = self._name.split('report.')[-1]
        report = report_obj._get_report_from_name(report_name)
        if docids:
            docs = self.env[report.model].browse(docids)
            tasks = []
            lang = self.env.lang
        else:
            docs = self.env[report.model].browse(data['project_id'])
            tasks = self.env['project.task'].browse(data['task_ids'])
            lang = data.get('forced_lang') or self.env.lang
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'tasks': tasks,
            'report': self,
            'forced_lang': lang,
            'conformity_options': self._get_conformity_options(lang),
        }
        return report_obj.render(report_name, docargs)

    def get_analysis_type(self, product):
        return 'chemical' if product.chemistry == 'chem' else 'mech_env'

    def display_legal_reference(self, tasks):
        """It is needed to display a legal reference section"""
        return any(tasks.filtered(
            lambda task: self.get_analysis_type(
                task.sale_line_id.product_id
            ) != 'mech_env'
        ))

    def task_field_info(self, fname):
        return self.env['project.task'].fields_get(
            allfields=[fname, ])[fname]

    def get_mech_env_details(self, task):
        details = {}
        for fname in self.mech_test_fields:
            content = task[fname]
            # an "empty" field contains u'<p><br></p>'
            if content and html2text(content).strip():
                info = self.task_field_info(fname)
                details['label'] = info['string']
                details['val'] = content
        return details
