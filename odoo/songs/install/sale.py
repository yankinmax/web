# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv


@anthem.log
def configure_sale_app(ctx):
    """Configure sale app"""

    sale_settings = ctx.env['sale.config.settings']

    vals = {
        'group_sale_delivery_address': 1,
        'group_discount_per_so_line': 1,
        'group_mrp_properties': 1,
        'sale_pricelist_setting': 'formula',
        'module_website_quote': 1,
        'sale_show_tax': 'total',
    }
    acs = sale_settings.create(vals)
    acs.execute()


@anthem.log
def import_maint_equipment(ctx):
    load_csv(ctx, 'data/install/maint.equipment.csv', 'maintenance.equipment')


@anthem.log
def import_product_extraction_type(ctx):
    load_csv(
        ctx, 'data/install/product.extraction.type.csv',
        'product.extraction.type')


@anthem.log
def import_product_method(ctx):
    load_csv(ctx, 'data/install/product.method.csv', 'product.method')


@anthem.log
def import_product_uom(ctx):
    load_csv(ctx, 'data/install/product.uom.csv', 'product.uom')


@anthem.log
def main(ctx):
    """ Configuring sales """
    configure_sale_app(ctx)
    import_maint_equipment(ctx)
    import_product_extraction_type(ctx)
    import_product_method(ctx)
    import_product_uom(ctx)
