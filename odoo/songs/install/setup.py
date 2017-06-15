# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import anthem
from ..common import define_settings


@anthem.log
def base_settings(ctx):
    """ base_settings """
    define_settings(
        ctx,
        'base.config.settings',
        {
            'group_light_multi_company': True,
            'module_inter_company_rules': True,
            'company_share_partner': False,
        })


@anthem.log
def sale_settings(ctx):
    """ sale_settings """
    define_settings(
        ctx,
        'sale.config.settings',
        {
            'sale_pricelist_setting': 'formula',
            'group_sale_pricelist': True,
            'group_pricelist_item': True,
            'group_discount_per_so_line': 1,
        })


@anthem.log
def main(ctx):
    base_settings(ctx)
    sale_settings(ctx)
