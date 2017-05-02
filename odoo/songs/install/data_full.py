# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


""" File for full (production) data

These songs will be called on integration and production server at the
installation.

NB: For the moment they are all calling demo data. Please change the path and
the comment when switching to production data.

"""


@anthem.log
def main(ctx):
    """ Loading full data """
