# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_users_csv


@anthem.log
def import_users(ctx):
    load_users_csv(ctx, 'data/install/res.users.csv')


@anthem.log
def main(ctx):
    """ Configuring users """
    import_users(ctx)
