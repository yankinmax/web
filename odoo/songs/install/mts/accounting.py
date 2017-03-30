# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def set_fiscalyear(ctx):
    values = {'date_start': '2017-01-01',
              'name': '2017',
              'date_end': '2017-12-31',
              'type_id': 1,
              'company_id': ctx.env.ref('base.main_company').id,
              'active': True,
              }
    create_or_update(ctx, 'date.range',
                     '__setup__.date_range_mts_2017', values)


@anthem.log
def main(ctx):
    """ Configuring accounting """
    set_fiscalyear(ctx)
