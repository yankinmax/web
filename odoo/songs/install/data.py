# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import anthem

from ..common import deferred_compute_parents
from ..common import deferred_import
from ..common import load_csv
from ..common import load_users_csv


@anthem.log
def import_groups(ctx):
    """ Importing groups """
    load_csv(ctx, 'data/install/01.groups.csv', 'res.groups', delimiter=';')


@anthem.log
def import_partners(ctx):
    """ Importing partners """
    load_csv(ctx, 'data/install/02.partners.csv', 'res.partner', delimiter=';')


@anthem.log
def import_users(ctx):
    """ Importing users """
    load_users_csv(ctx, 'data/install/03.users.csv', delimiter=';')


@anthem.log
def import_centers(ctx):
    """ Importing centers """
    deferred_import(
        ctx, 'res.company', 'data/install/04.centers.csv', delimiter=';'
    )


@anthem.log
def location_compute_parents(ctx):
    """Compute parent_left, parent_right"""
    deferred_compute_parents(ctx, 'stock.location')


@anthem.log
def import_users_dependances(ctx):
    """ Importing users dependances """
    load_csv(
        ctx,
        'data/install/05.users_dependances.csv',
        'res.users',
        delimiter=';'
    )


@anthem.log
def import_centers_dependances(ctx):
    """ Importing centers dependances """
    load_csv(
        ctx,
        'data/install/06.centers_dependances.csv',
        'res.company',
        delimiter=';'
    )


@anthem.log
def import_centers_horaires(ctx):
    """ Importing centers horaires """
    load_csv(
        ctx,
        'data/install/07.centers_horaires.csv',
        'res.company.schedule',
        delimiter=';'
    )


@anthem.log
def import_centers_pts(ctx):
    """ Importing centers pts """
    load_csv(
        ctx,
        'data/install/08.centers_pts.csv',
        'res.company.phototherapist',
        delimiter=';'
    )


@anthem.log
def import_partners_dependances(ctx):
    """ Importing partner dependances """
    load_csv(
        ctx,
        'data/install/09.partners_dependances.csv',
        'res.partner',
        delimiter=';'
    )


@anthem.log
def survey_survey_import(ctx):
    """ survey_survey_import """
    load_csv(ctx, 'data/setup/survey.survey.csv', 'survey.survey')


@anthem.log
def survey_page_import(ctx):
    """ survey_page_import """
    load_csv(ctx, 'data/setup/survey.page.csv', 'survey.page')


@anthem.log
def survey_question_import(ctx):
    """ survey_question_import """
    load_csv(ctx, 'data/setup/survey.question.csv', 'survey.question')


@anthem.log
def product_category_import(ctx):
    """ product_category_import """
    load_csv(
        ctx,
        'data/setup/product.category.csv',
        'product.category',
        delimiter=';'
    )


@anthem.log
def product_product_import(ctx):
    """ product_product_import """
    load_csv(ctx, 'data/install/10.product - all.csv', 'product.product')

    load_csv(ctx, 'data/install/11.product - new.csv', 'product.product')


@anthem.log
def sale_discount_program_import(ctx):
    """ sale_discount_program_import """
    load_csv(
        ctx, 'data/setup/sale.discount.program.csv', 'sale.discount.program'
    )


@anthem.log
def main(ctx):
    """ Loading data """
    import_groups(ctx)
    import_partners(ctx)
    import_users(ctx)
    import_centers(ctx)

    location_compute_parents(ctx)

    import_users_dependances(ctx)
    import_centers_dependances(ctx)
    import_centers_horaires(ctx)
    import_centers_pts(ctx)
    import_partners_dependances(ctx)

    survey_survey_import(ctx)
    survey_page_import(ctx)
    survey_question_import(ctx)
    product_category_import(ctx)
    product_product_import(ctx)
    sale_discount_program_import(ctx)
