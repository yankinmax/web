# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv
from ..install.post import setup_mte_reports_info


@anthem.log
def create_product_categories(ctx):
    """create MTE categories from CSV"""
    path = 'data/install/mte/product_category_MT.csv'
    load_csv(ctx, path, 'product.category')


@anthem.log
def update_sale_settings(ctx):
    """Field 'Tax Display' shoud be B2C"""
    sale_settings = ctx.env["sale.config.settings"]
    # already present in songs/install/sale.py BSMTS-217
    vals = {
        'sale_show_tax': 'total'
    }
    setting = sale_settings.create(vals)
    setting.execute()


@anthem.log
def main(ctx):
    """create categories"""
    create_product_categories(ctx)
    update_sale_settings(ctx)
    """update logo"""
    setup_mte_reports_info(ctx)
