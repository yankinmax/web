# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream
from anthem.lyrics.records import create_or_update
from ..common import req

""" File for demo data

These songs will be called when the mode is 'demo', we should import only
excerpt of data, while the full data is only imported in the 'full' mode.

"""


@anthem.log
def import_customers(ctx):
    """ Importing customers from csv """
    content = resource_stream(req, 'data/demo/customers.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_employee(ctx):
    """ Importing employee from csv """
    content = resource_stream(req, 'data/demo/hr.employee.csv')
    load_csv_stream(ctx, 'hr.employee', content, delimiter=',')


@anthem.log
def update_company(ctx):
    """ Updating company """
    with ctx.log(u'Update company number'):
        values = {
            'phone': "+41 32 968 08 16",
        }
        create_or_update(ctx, 'res.company',
                         'base.main_company',
                         values)


@anthem.log
def import_partner_contact(ctx):
    """ Importing partner_contact from csv """
    content = resource_stream(req, 'data/demo/res.partner.contact.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_partner(ctx):
    """ Importing partner from csv """
    content = resource_stream(req, 'data/demo/res.partner.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_users(ctx):
    """ Importing users from csv """
    content = resource_stream(req, 'data/demo/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading demo data """
    update_company(ctx)
    import_users(ctx)
    import_partner(ctx)
    import_partner_contact(ctx)
    import_employee(ctx)
    import_customers(ctx)
