# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv


@anthem.log
def create_product_categories(ctx):
    """create MTE categories from CSV"""
    path = 'data/install/mte/product_category_MTE.csv'
    load_csv(ctx, path, 'product.category')


@anthem.log
def main(ctx):
    """create categories"""
    create_product_categories(ctx)
