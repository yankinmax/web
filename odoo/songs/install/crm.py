# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def disable_base_sales_teams(ctx):
    """Disable base sales teams"""
    ctx.env.ref('sales_team.team_sales_department').active = False
    ctx.env.ref('sales_team.salesteam_website_sales').active = False


@anthem.log
def main(ctx):
    """ Configuring CRM """
    disable_base_sales_teams(ctx)
