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
def import_partner(ctx):
    """ Importing full partner from csv """
    content = resource_stream(req, 'data/install/res.partner.csv')
    load_csv_stream(ctx, 'res.partner', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading full data """
    import_partner(ctx)
