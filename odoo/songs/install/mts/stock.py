# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ...common import load_warehouses


@anthem.log
def settings_MTS(ctx):
    """ Configure Warehouse settings"""
    ctx.env['stock.config.settings'].create({
        'company_id': ctx.env.ref('base.main_company').id,
        # enable multi locations
        'group_stock_multi_locations': True,
    }).execute()


@anthem.log
def load_warehouses_MTS(ctx):
    load_warehouses(
        ctx, 'base.main_company',
        'data/install/mts/stock.warehouse.MTS.csv')


@anthem.log
def main(ctx):
    settings_MTS(ctx)
    load_warehouses_MTS(ctx)
