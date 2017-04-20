# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

company_xmlids = [
    '__setup__.company_mte',
    'base.main_company',
]


def companies(ctx):
    companies = ctx.env['res.company']
    for xmlid in company_xmlids:
        companies |= ctx.env.ref(xmlid)
    return companies


coa_dict = {
    '__setup__.company_mte': 'l10n_ch.l10nch_chart_template',
    'base.main_company': 'l10n_ch.l10nch_chart_template',
}
