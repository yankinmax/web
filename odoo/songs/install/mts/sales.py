# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem

from ...common import load_csv
from ...common import set_sale_conditions


@anthem.log
def set_sale_conditions_MTS(ctx):
    company = ctx.env.ref('base.main_company')
    conditions = [
        # lang, filepath
        ('en_US', 'data/install/mts/mts_sale_conditions_en.html'),
        ('fr_FR', 'data/install/mts/mts_sale_conditions_fr.html'),
    ]
    set_sale_conditions(ctx, company, conditions)


@anthem.log
def import_product_category_MTS(ctx):
    path = 'data/install/mts/product.category.MTS.csv'
    load_csv(ctx, path, 'product.category')


@anthem.log
def import_product_template_MTS(ctx):
    path = 'data/install/mts/product.template.MTS.csv'
    load_csv(ctx, path, 'product.template')


@anthem.log
def import_product_sellers_MTS(ctx):
    # this must run after partners have been imported
    path = 'data/install/mts/product.product_sellers_rel.MTS.csv'
    load_csv(ctx, path, 'product.template')


@anthem.log
def main(ctx):
    """ Configuring sales MTS main """
    set_sale_conditions_MTS(ctx)
    import_product_category_MTS(ctx)
    import_product_template_MTS(ctx)


@anthem.log
def full(ctx):
    """ Configuring sales MTS full """
    import_product_sellers_MTS(ctx)


@anthem.log
def demo(ctx):
    """ Configuring sales MTS demo """
    import_product_category_MTS(ctx)
    import_product_template_MTS(ctx)
