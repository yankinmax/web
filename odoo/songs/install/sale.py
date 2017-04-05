# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


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
    }
    acs = sale_settings.create(vals)
    acs.execute()


@anthem.log
def main(ctx):
    """ Configuring sales """
    configure_sale_app(ctx)
