# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv

""" File for demo data

These songs will be called when the mode is 'demo', we should import only
excerpt of data, while the full data is only imported in the 'full' mode.

"""


# TODO: is this needed at all?
@anthem.log
def import_customers(ctx):
    """ Importing customers from csv """
    load_csv(ctx, 'data/demo/customers.csv', 'res.partner')


@anthem.log
def import_projects(ctx):
    """ Importing projects from csv """
    load_csv(ctx, 'data/demo/project.project.csv', 'project.project')


@anthem.log
def import_project_tasks(ctx):
    """ Importing project tasks from csv """
    load_csv(ctx, 'data/demo/project.task.csv', 'project.task')


@anthem.log
def import_partners(ctx):
    """ Importing demo partner from csv """
    load_csv(ctx, 'data/demo/res.partner.csv', 'res.partner')


@anthem.log
def import_product_template_MT(ctx):
    load_csv(ctx, 'data/demo/product.template.MT.csv', 'product.template')


@anthem.log
def import_product_substance_MT(ctx):
    load_csv(ctx, 'data/demo/product.substance.MT.csv', 'product.substance')


@anthem.log
def import_product_substance_rel_MT(ctx):
    load_csv(ctx, 'data/demo/product.product_substances_rel.MT.csv',
             'product.template')


@anthem.log
def main(ctx):
    """ Loading demo data """
    import_partners(ctx)
    import_projects(ctx)
    import_project_tasks(ctx)
    import_product_template_MT(ctx)
    import_product_substance_MT(ctx)
    import_product_substance_rel_MT(ctx)
