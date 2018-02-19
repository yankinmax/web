# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def settings_inventory(ctx):
    """ Configure stock production lot settings.
        Base setup has been updated """
    ctx.env['stock.config.settings'].create(
        {'group_stock_production_lot': 1}
    ).execute()


@anthem.log
def pre(ctx):
    settings_inventory(ctx)
