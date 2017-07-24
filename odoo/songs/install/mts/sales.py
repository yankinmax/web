# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem

from ...common import req, load_csv


@anthem.log
def set_sale_conditions(ctx):
    """ Set sale description """
    company = ctx.env.ref('base.main_company')
    note = resource_stream(
        req,
        'data/install/mts/mts_sale_conditions_2017_04.html')
    company.sale_note = note.read()


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
    path = 'data/install/mts/product.product_sellers_rel.MTS.csv'
    load_csv(ctx, path, 'product.template')


@anthem.log
def main(ctx):
    """ Configuring sales settings MTS """
    set_sale_conditions(ctx)
    import_product_category_MTS(ctx)
    import_product_template_MTS(ctx)
    # TODO: activate this once stock setup is done
    # import_product_sellers_MTS(ctx)
