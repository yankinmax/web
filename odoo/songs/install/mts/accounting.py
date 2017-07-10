# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update
from ...common import load_chart_of_accounts


@anthem.log
def set_fiscalyear(ctx):
    for year in ['2010', '2011', '2012', '2013', '2014', '2015', '2016',
                 '2017', '2018']:
        values = {'date_start': year + '-01-01',
                  'name': year,
                  'date_end': year + '-12-31',
                  'type_id': 1,
                  'company_id': ctx.env.ref('base.main_company').id,
                  'active': True,
                  }
        create_or_update(ctx, 'date.range',
                         '__setup__.date_range_mts_' + year, values)


@anthem.log
def import_chart_of_account(ctx):
    """ Customize accounts """
    load_chart_of_accounts(ctx, 'base.main_company',
                           'data/install/mts/account.account.csv')


@anthem.log
def main(ctx):
    """ Configuring accounting """
    set_fiscalyear(ctx)
    import_chart_of_account(ctx)
