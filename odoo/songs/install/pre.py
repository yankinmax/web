# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os

from base64 import b64encode
from pkg_resources import resource_string

import anthem
from anthem.lyrics.records import create_or_update

from ..common import req


@anthem.log
def setup_company_minimal(ctx):
    """ Setup company minimal """
    company = ctx.env.ref('base.main_company')
    company.name = "Depil'Tech Holding"


@anthem.log
def setup_company(ctx):
    """ Configuring company data """
    company = ctx.env.ref('base.main_company')
    company.country_id = ctx.env.ref('base.fr').id

    # load logo on company
    logo_content = resource_string(req, 'data/images/logo.png')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo

    with ctx.log(u'Configuring company'):
        values = {
            'name': 'Agencies Holding',
            'country_id': ctx.env.ref('base.fr').id,
            'phone': '+33 00 000 00 00',
            'fax': '+33 00 000 00 00',
            'company_type': 'company',
        }
        create_or_update(ctx, 'res.partner',
                         'scenario.user_agencyHolding_res_partner',
                         values)
        values = {
            'name': 'Agencies Holding',
            'country_id': ctx.env.ref('base.fr').id,
            'phone': '+33 00 000 00 00',
            'fax': '+33 00 000 00 00',
            'currency_id': ctx.env.ref('base.EUR').id,
            'can_create_product': True,
            'partner_id':
                ctx.env.ref('scenario.user_agencyHolding_res_partner').id,
            'parent_id': company.id,
        }
        create_or_update(ctx, 'res.company',
                         'scenario.company_agencyHolding',
                         values)


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR', 'es_MX'):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([('code', '=', 'fr_FR')]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
        'thousands_sep': ',',
    })


@anthem.log
def admin_user_password(ctx):
    """ Changing admin password """
    # To get an encrypted password:
    # $ docker-compose run --rm odoo python -c \
    # "from passlib.context import CryptContext; \
    #  print CryptContext(['pbkdf2_sha512']).encrypt('my_password')"
    if os.environ.get('RUNNING_ENV') == 'dev':
        ctx.log_line('Not changing password for dev RUNNING_ENV')
        return
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$19000$xBiDsLY2BqDU.n8PYew9Bw$O3hHKc9f.OyeDPD2A6lvf'
        'aebpmIYjB.8HGOABIh5Cc1xE387/Di.A0ok/qF8WzEyjzlEM67sm.VkhOBEdcJcBg'
    )


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_company_minimal(ctx)
    setup_language(ctx)
    admin_user_password(ctx)
