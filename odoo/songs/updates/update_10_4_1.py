# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import anthem


@anthem.log
def update_sale_workflow(ctx):
    # added to /install/sale_workflow.py
    create_invoice_filter = ctx.env.ref(
        'sale_automatic_workflow.automatic_workflow_create_invoice_filter'
    )
    create_invoice_filter.domain = (
        "[('state', 'in', ['sale', 'done', 'waiting_calculator']), "
        "('invoice_status', '=', 'to invoice'), "
        "('partner_company_type', '=', 'agency_customer'), "
        "('order_line.qty_to_invoice', '>', 0)]")


@anthem.log
def main(ctx):
    """Update sale workflow configuration."""
    update_sale_workflow(ctx)
