# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv

""" Data loaded in all modes

The data loaded here will be loaded in the 'demo' and
'full' modes.

"""


@anthem.log
def create_engagements_bi_sql_view(ctx):
    """ Create engagement BI SQL view:
        * Load the view from SQL
        * Validate the SQL view
        * Call actions to create the ORM model, views, menu and actions
          related to the SQL view """
    load_csv(ctx, 'data/install/bi.sql.view.csv', 'bi.sql.view')
    bi_view = ctx.env.ref('__setup__.bi_sql_view_engagements')
    bi_view.button_validate_sql_expression()
    bi_view.button_create_sql_view_and_model()

    group_by_fields = bi_view.bi_sql_view_field_ids.filtered(
        lambda f: f.name in ['x_invoice_status', 'x_partner', 'x_ref_date',
                             'x_currency']
    )
    group_by_fields.write({'is_group_by': True})
    bi_view.button_create_ui()


@anthem.log
def main(ctx):
    """ Loading data """
    create_engagements_bi_sql_view(ctx)
