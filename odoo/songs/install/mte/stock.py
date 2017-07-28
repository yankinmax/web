# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ...common import load_warehouses


@anthem.log
def load_warehouses_MT(ctx):
    load_warehouses(
        ctx, '__setup__.company_mte',
        'data/install/mte/stock.warehouse.MT.csv')


@anthem.log
def main(ctx):
    load_warehouses_MT(ctx)
