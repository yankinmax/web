# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import anthem


@anthem.log
def uninstall_dj_modules(ctx):
    """ Uninstalling DJ modules """
    ctx.env['ir.module.module'].search(
        [('name', 'like', '%dj%'), ('state', '=', 'installed')]
    ).button_immediate_uninstall()


@anthem.log
def main(ctx):
    """ Applying update 10.3.1 """
    uninstall_dj_modules(ctx)
