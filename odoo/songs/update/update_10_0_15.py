# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv, load_file_content


@anthem.log
def create_product_categories(ctx):
    """create MTE categories from CSV"""
    path = 'data/install/mte/product_category_MTE.csv'
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
def change_mte_report_logo(ctx):
    """Update mte report logo"""
    mte = ctx.env.ref('__setup__.company_mte')
    mte_logo = 'local-src/mtsmte_reports/static/src/img/mte_logo_new.png'
    mte.write({
        'report_logo': load_file_content(mte_logo).read().encode('base64'),
        'report_show_address_header': True,
    })
    ctx.log_line('MTE report info updated')


@anthem.log
def main(ctx):
    """create categories"""
    create_product_categories(ctx)
    update_sale_settings(ctx)
    """update logo"""
    change_mte_report_logo(ctx)
