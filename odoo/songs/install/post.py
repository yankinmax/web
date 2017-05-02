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


@anthem.log
def main(ctx):
    """ Post """
    setup_multi_company(ctx)
    add_company_to_user(ctx)
    create_incoming_mail_server(ctx)
