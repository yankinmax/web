# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def setup_language_de(ctx):
    code = 'de_DE'
    installed = ctx.env['res.lang'].with_context(
        active_test=True).search([('code', '=', code)])
    if not installed:
        ctx.log_line('Installing German...')
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
        ctx.env['res.lang'].search([('code', '=', code)]).write({
            'grouping': [3, 0],
            'date_format': '%d/%m/%Y',
        })


@anthem.log
def pre(ctx):
    setup_language_de(ctx)
