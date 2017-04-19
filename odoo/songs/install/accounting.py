# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem

from . import base_vars


@anthem.log
def base_conf(ctx):
    """ Configuring analytic for purchase/sale """
    account_settings = ctx.env['account.config.settings']
    for company_xml_id, coa in base_vars.coa_dict.iteritems():
        company = ctx.env.ref(company_xml_id)
        acs = account_settings.with_context(company_id=company.id).create(
            {'group_analytic_accounting': True,
             'group_multi_currency': True,
             'group_analytic_account_for_purchases': True,
             'tax_calculation_rounding_method': 'swedish_round_globally',
             }
        )
        acs.execute()


@anthem.log
def main(ctx):
    """ Configuring accounting """
    base_conf(ctx)
