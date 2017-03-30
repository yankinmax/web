# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream
from ..common import req


""" File for full (production) data

These songs will be called on integration and production server at the
installation.

NB: For the moment they are all calling demo data. Please change the path and
the comment when switching to production data.

"""


@anthem.log
def import_customers(ctx):
    """ Importing customers from csv """
    content = resource_stream(req, 'data/demo/customers.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_employee(ctx):
    """ Importing demo employee from csv """
    content = resource_stream(req, 'data/demo/hr.employee.csv')
    load_csv_stream(ctx, 'hr.employee', content, delimiter=',')


@anthem.log
def import_partner_contact(ctx):
    """ Importing demo partner_contact from csv """
    content = resource_stream(req, 'data/demo/res.partner.contact.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_partner(ctx):
    """ Importing demo partner from csv """
    content = resource_stream(req, 'data/demo/res.partner.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def import_users(ctx):
    """ Importing demo users from csv """
    content = resource_stream(req, 'data/demo/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading demo data """
    import_users(ctx)
    import_partner(ctx)
    import_partner_contact(ctx)
    import_employee(ctx)
    import_customers(ctx)
