# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from openerp import models, fields, api


class ReportPageEndNote(models.Model):
    _name = 'report.page.endnote'
    _description = 'Manage global page endnotes'

    def _get_default_country(self):
        return self.env.user.company_id.country_id.id

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    country_id = fields.Many2one(comodel_name='res.country',
                                 default=_get_default_country,
                                 required=True)
    content = fields.Html(required=True, translate=True)
    report_ids = fields.Many2many(
        comodel_name='ir.actions.report.xml',
        domain=[('report_type', 'in', ('qweb-pdf', 'qweb-html'))]
    )

    @api.multi
    def button_show_created_views(self):
        self.ensure_one()
        try:
            report_names = self.report_ids.mapped('report_name')
            report_names1 = map(lambda a: a.split('.')[1]+"%_page_endnote",
                                report_names)
            act_window_obj = self.env['ir.actions.act_window']
            view_action = act_window_obj.for_xml_id('base', 'action_ui_view')
            domain = [('type', '=', 'qweb')]
            views = self.env['ir.ui.view']
            view_ids = []
            for r in report_names1:
                view_ids.extend(
                    views.search(domain + [('name', 'ilike', r)]).ids
                )
            if view_ids:
                domain2 = [('id', 'in', list(set(view_ids)))]
                view_action['domain'] = domain2
                return view_action
            else:
                return False
        except:
            return False

    @api.model
    def render(self, report_object):
        s_args = [
            ('country_id', '=', report_object.company_id.country_id.id),
        ]
        endnote = self.search(s_args, limit=1)
        if self.env.context.get('lang', False):
            endnote = endnote.with_context(lang=self.env.context.get('lang'))
        return endnote.content

    @api.model
    @api.returns('report.page.endnote')
    def create(self, values):
        new_one = super(ReportPageEndNote, self).create(values)
        new_one.check_reports()
        return new_one

    @api.multi
    def write(self, values):
        """
        """
        super(ReportPageEndNote, self).write(values)
        self.check_reports()
        return True

    @api.multi
    def construct_arch(self, inherited_view):
        # try to find the variable used to represent the current object the
        # report is rendering (usually 'o' but can be 'doc' or 'd' or whatever)
        view_variable = 'o'
        # parse view to find a t-field attribute
        if inherited_view:
            regex = 't-field="(.*)"\s+'
            match = re.search(regex, inherited_view.arch)
            if match.groups():
                # we found one so we can parse the expression of the t-field
                view_variable = match.groups()[0].split('.')[0]

        # create the view
        m = '<div class="page" position="inside">'
        m += '<t t-set="xx" t-value="%s"/>' % view_variable
        m += '<t t-call="report_page_endnote.page_endnote"/>'
        m += '</div>'
        return m

    @api.multi
    def check_reports(self):
        """
        """
        report_views = self.env['ir.ui.view']
        for rec in self:
            for rep in rec.report_ids:
                normal_name = rep.report_name.split('.')[1]
                name_search = normal_name + "%_page_endnote"
                s_args = [('type', '=', 'qweb')]
                inherit = self.env['ir.ui.view'].search(
                    s_args + [('name', 'ilike', normal_name)]
                )
                inherit_v = False
                for v in inherit:
                    if '<div class="page">' in v.arch:
                        inherit_v = v
                    else:
                        continue

                if (not report_views.search(
                        [('name', 'ilike', name_search)] + s_args, limit=1)):
                    # create one
                    self.env['ir.actions.report.xml']._create_qweb(
                        name_search.replace('%', ''),
                        name_search.replace('%', ''),
                        'report_page_endnote_data',
                        '',
                        self.construct_arch(inherit_v))
                    view = self.env.ref("%s.%s" % ('report_page_endnote_data',
                                                   name_search.replace('%', '')
                                                   )
                                        )
                    if inherit_v:
                        view.write({'inherit_id': inherit_v.id,
                                   'mode': 'extension'})

        return True
