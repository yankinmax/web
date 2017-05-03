# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update

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
def main(ctx):
    """ Post """
    setup_multi_company(ctx)
    add_company_to_user(ctx)
    create_incoming_mail_server(ctx)
    setup_mail_catchall_domain(ctx)
