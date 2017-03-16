# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

# from base64 import b64encode
from pkg_resources import resource_stream

import os
import anthem

from anthem.lyrics.loaders import load_csv_stream

from ..common import req


@anthem.log
def setup_company(ctx):
    """ Setup companies """
    # load logo on company
    # logo_content = resource_string(req, 'data/images/company_main_logo.png')
    # b64_logo = b64encode(logo_content)
    # company.logo = b64_logo

    content = resource_stream(req, 'data/install/res.company.csv')
    load_csv_stream(ctx, 'res.company', content, delimiter=',')


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR',):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
    })


@anthem.log
def admin_user_password(ctx):
    """ Changing admin password """
    if os.environ.get('RUNNING_ENV') == 'dev':
        ctx.log_line('Not changing password for dev RUNNING_ENV')
        return
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$19000$/v9f6/3/fw8BoFSqdW4t5Q$qT96ieTiXgNT8I/ePs2zd'
        'oAc66EVy8IjToQxUxOaXVwKLwCGWY9EBu3TtpSvqzcTqnULPNOGH63x4j261Aia7A'

    )


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_company(ctx)
    setup_language(ctx)
    admin_user_password(ctx)
