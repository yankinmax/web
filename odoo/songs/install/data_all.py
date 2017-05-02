# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem

from anthem.lyrics.loaders import load_csv_stream
from ..common import req, load_users_csv

""" Data loaded in all modes

The data loaded here will be loaded in the 'demo' and
'full' modes.

"""


@anthem.log
def import_users(ctx):
    """ Importing demo users from csv """
    content = resource_stream(req, 'data/demo/res.users.csv')
    load_users_csv(ctx, content, delimiter=',')


@anthem.log
def import_partner(ctx):
    """ Importing demo partner from csv """
    content = resource_stream(req, 'data/demo/res.partner.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_partner_contact(ctx):
    """ Importing demo partner_contact from csv """
    content = resource_stream(req, 'data/demo/res.partner.contact.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_employee(ctx):
    """ Importing demo employee from csv """
    content = resource_stream(req, 'data/demo/hr.employee.csv')
    load_csv_stream(ctx, 'hr.employee', content, delimiter=',')


@anthem.log
def import_crm_teams(ctx):
    """ Importing CRM teams from CSV """
    content = resource_stream(req, 'data/install/mte/crm.team.csv')
    load_csv_stream(ctx, 'crm.team', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading data """
    import_users(ctx)
    import_partner(ctx)
    import_partner_contact(ctx)
    import_employee(ctx)
    import_crm_teams(ctx)
