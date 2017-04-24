# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream
from ..common import req


@anthem.log
def import_groups(ctx):
    """ Importing groups """
    content = resource_stream(
        req, 'data/install/01.groups.csv'
    )
    load_csv_stream(ctx, 'res.groups', content, delimiter=';')


@anthem.log
def import_partners(ctx):
    """ Importing partners """
    content = resource_stream(
        req, 'data/install/02.partners.csv'
    )
    load_csv_stream(ctx, 'res.partner', content, delimiter=';')


@anthem.log
def import_users(ctx):
    """ Importing users """

    load_ctx = ctx.env.context.copy()
    load_ctx.update({'no_reset_password': True})
    users_model = ctx.env['res.users'].with_context(load_ctx)

    content = resource_stream(
        req, 'data/install/03.users.csv'
    )
    load_csv_stream(ctx, users_model, content, delimiter=';')


@anthem.log
def import_centers(ctx):
    """ Importing centers """

    load_ctx = ctx.env.context.copy()
    load_ctx.update({'defer_parent_store_computation': 'manually'})
    company_model = ctx.env['res.company'].with_context(load_ctx)

    content = resource_stream(
        req, 'data/install/04.centers.csv'
    )
    load_csv_stream(ctx, company_model, content, delimiter=';')


@anthem.log
def location_compute_parents(ctx):
    """Compute parent_left, parent_right"""
    ctx.env['stock.location']._parent_store_compute()


@anthem.log
def import_users_dependances(ctx):
    """ Importing users dependances """
    content = resource_stream(
        req, 'data/install/05.users_dependances.csv'
    )
    load_csv_stream(ctx, 'res.users', content, delimiter=';')


@anthem.log
def import_centers_dependances(ctx):
    """ Importing centers dependances """
    content = resource_stream(
        req, 'data/install/06.centers_dependances.csv'
    )
    load_csv_stream(ctx, 'res.company', content, delimiter=';')


@anthem.log
def import_centers_horaires(ctx):
    """ Importing centers horaires """
    content = resource_stream(
        req, 'data/install/07.centers_horaires.csv'
    )
    load_csv_stream(ctx, 'res.company.schedule', content, delimiter=';')


@anthem.log
def import_centers_pts(ctx):
    """ Importing centers pts """
    content = resource_stream(
        req, 'data/install/08.centers_pts.csv'
    )
    load_csv_stream(ctx, 'res.company.phototherapist', content, delimiter=';')


@anthem.log
def import_partners_dependances(ctx):
    """ Importing partner dependances """
    content = resource_stream(
        req, 'data/install/09.partners_dependances.csv'
    )
    load_csv_stream(ctx, 'res.partner', content, delimiter=';')


@anthem.log
def survey_survey_import(ctx):
    """ survey_survey_import """
    content = resource_stream(req, 'data/setup/survey.survey.csv')
    load_csv_stream(ctx, 'survey.survey', content, delimiter=',')


@anthem.log
def survey_page_import(ctx):
    """ survey_page_import """
    content = resource_stream(req, 'data/setup/survey.page.csv')
    load_csv_stream(ctx, 'survey.page', content, delimiter=',')


@anthem.log
def survey_question_import(ctx):
    """ survey_question_import """
    content = resource_stream(req, 'data/setup/survey.question.csv')
    load_csv_stream(ctx, 'survey.question', content, delimiter=',')


@anthem.log
def product_category_import(ctx):
    """ product_category_import """
    content = resource_stream(req, 'data/setup/product.category.csv')
    load_csv_stream(ctx, 'product.category', content, delimiter=';')


@anthem.log
def product_product_import(ctx):
    """ product_product_import """
    content = resource_stream(req, 'data/install/10.product - all.csv')
    load_csv_stream(ctx, 'product.product', content, delimiter=',')

    content = resource_stream(req, 'data/install/11.product - new.csv')
    load_csv_stream(ctx, 'product.product', content, delimiter=',')


@anthem.log
def sale_discount_program_import(ctx):
    """ sale_discount_program_import """
    content = resource_stream(req, 'data/setup/sale.discount.program.csv')
    load_csv_stream(ctx, 'sale.discount.program', content, delimiter=',')


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
