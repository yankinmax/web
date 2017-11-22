# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update

from ..common import load_file_content
from . import base_vars


@anthem.log
def setup_multi_company(ctx):
    """ Configuring multi-company """
    base_settings = ctx.env['base.config.settings']
    base_settings.create(
        {'group_multi_company': True,
         'company_share_partner': False,
         'company_share_product': False,
         }
    ).execute()


@anthem.log
def company_dj_set_aka(ctx):
    # cannot set company aka via company csv import
    # as it happens in `pre` and base_dj is not installed yet
    ctx.env.ref('base.main_company').aka = 'MTS'
    ctx.env.ref('__setup__.company_mte').aka = 'MT'


@anthem.log
def add_company_to_user(ctx):
    """ Add companies to users """
    ctx.env.ref('base.user_root').write({
        'company_ids': [(6, 0, [base_vars.companies(ctx).ids])],
    })


@anthem.log
def create_incoming_mail_server(ctx):
    """ Create incoming mail server """
    create_or_update(ctx, 'fetchmail.server',
                     '__setup__.fetchmail_mail_in_mtsmte',
                     {'name': 'mail_in_mtsmte'})


def setup_mail_catchall_domain(ctx):
    """ Setup e-mail catchall domains """
    domains = {
        'base.main_company': 'mtssa.ch',
        '__setup__.company_mte': 'metallo-tests.ch',
    }
    current_company = ctx.env.user.company_id
    try:
        for company_xmlid in base_vars.company_xmlids:
            company = ctx.env.ref(company_xmlid)
            domain = domains[company_xmlid]
            ctx.env.user.company_id = company
            ctx.env['ir.config_parameter'].set_param(
                'mail.catchall.domain',
                domain
            )
    finally:
        ctx.env.user.company_id = current_company


@anthem.log
def setup_mts_reports_info(ctx):
    mts = ctx.env.ref('base.main_company')
    mts_logo = 'local-src/mtsmte_reports/static/src/img/mts_logo.jpg'
    if not mts.report_logo:
        mts.write({
            'report_logo': load_file_content(mts_logo).read().encode('base64'),
            'report_show_address_header': False,
        })
        ctx.log_line('MTS report info updated')


@anthem.log
def setup_mte_reports_info(ctx):
    mte = ctx.env.ref('__setup__.company_mte')
    mte_logo = 'local-src/mtsmte_reports/static/src/img/mte_logo.png'
    if not mte.report_logo:
        mte.write({
            'report_logo': load_file_content(mte_logo).read().encode('base64'),
            'report_show_address_header': True,
        })
        ctx.log_line('MTE report info updated')


@anthem.log
def main(ctx):
    """ Post """
    setup_multi_company(ctx)
    company_dj_set_aka(ctx)
    add_company_to_user(ctx)
    create_incoming_mail_server(ctx)
    setup_mail_catchall_domain(ctx)
    setup_mts_reports_info(ctx)
    setup_mte_reports_info(ctx)
