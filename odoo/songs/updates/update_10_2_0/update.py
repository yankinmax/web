# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def update_lead_action_datetime(ctx):

    leads = ctx.env['crm.lead'].search([
        ('date_action', '!=', False),
    ])
    for lead in leads:
        lead.write({
            'datetime_action':
                lead.date_action + ' 10:00:00'  # Will be 12:00 with timezone
        })


@anthem.log
def main(ctx):
    """ Main: update 10.2.0 """
    update_lead_action_datetime(ctx)
