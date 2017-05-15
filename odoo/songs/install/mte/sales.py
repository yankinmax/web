# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem

from ...common import req


@anthem.log
def set_sale_conditions(ctx):
    """ Set sale description """
    sales_settings = ctx.env['sale.config.settings']
    company = ctx.env.ref('__setup__.company_mte')
    note = resource_stream(
        req,
        'data/install/mte/mte_sales_conditions_2017.html')
    scs = sales_settings.with_context(company_id=company.id).create(
        {'sale_note': note.read()}
    )
    scs.execute()


@anthem.log
def main(ctx):
    """ Configuring Sales settings MTE """
    set_sale_conditions(ctx)
