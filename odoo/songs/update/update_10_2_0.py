# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def update_lang(ctx):
    """Set dot as a decimal delimiter for all active languages.
    """
    active_langs = ctx.env["res.lang"].search(
        [('active', '=', True)]
    )
    active_langs.write({
        "decimal_point": ".",
    })


@anthem.log
def main(ctx):
    update_lang(ctx)
