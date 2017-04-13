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
    # TODO : Voir le groupe base.group_configuration qui a été enlevé
    # TODO : Voir le groupe base.group_light_multi_company qui a été enlevé
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
    # TODO : Voir le VAT number FR9812708097 qui a été enlevé

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
def main_first_data(ctx):
    """ Loading data """
    import_groups(ctx)
    import_partners(ctx)
    import_users(ctx)
    import_centers(ctx)
    location_compute_parents(ctx)


@anthem.log
def main_others_data(ctx):
    """ Loading data """
    import_users_dependances(ctx)
    import_centers_dependances(ctx)
    import_centers_horaires(ctx)
    import_centers_pts(ctx)
    import_partners_dependances(ctx)
