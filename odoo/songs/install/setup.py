# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import anthem
from anthem.lyrics.records import create_or_update
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
def discount_pricelist(ctx):
    """ discount_pricelist """
    values = {
        'name': 'Parrainage',
        'discount_policy': 'without_discount',
        'item_ids': False,
    }
    create_or_update(ctx, 'product.pricelist',
                     'scenario.pricelist_sponsorship',
                     values)

    values = {
        'pricelist_id': ctx.env.ref('scenario.pricelist_sponsorship').id,
        'applied_on': '3_global',
        'compute_price': 'percentage',
        'percent_price': 10,
    }
    create_or_update(ctx, 'product.pricelist.item',
                     'scenario.pricelist_sponsorship_item1',
                     values)

    values = {
        'name': 'Code promo',
        'discount_policy': 'without_discount',
        'item_ids': False,
    }
    create_or_update(ctx, 'product.pricelist',
                     'scenario.pricelist_code_promo',
                     values)

    values = {
        'pricelist_id': ctx.env.ref('scenario.pricelist_code_promo').id,
        'applied_on': '3_global',
        'compute_price': 'percentage',
        'percent_price': 10,
    }
    create_or_update(ctx, 'product.pricelist.item',
                     'scenario.pricelist_code_promo_item1',
                     values)


@anthem.log
def main(ctx):
    base_settings(ctx)
    sale_settings(ctx)
    discount_pricelist(ctx)
