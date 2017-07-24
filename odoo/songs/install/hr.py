# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv


@anthem.log
def import_employees(ctx):
    load_csv(ctx, 'data/install/hr.employee.csv', 'hr.employee')


@anthem.log
def main(ctx):
    """ Configuring HR """
    import_employees(ctx)
