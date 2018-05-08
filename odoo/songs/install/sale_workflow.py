# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def sale_workflow_configuration(ctx):
    # Overrides the configuration in song update_10.1.1
    # as this is definitely an installation step
    automatic_workflow = ctx.env.ref(
        'sale_automatic_workflow.automatic_validation'
    )
    automatic_workflow.validate_order = False
    create_invoice_filter = ctx.env.ref(
        'sale_automatic_workflow.automatic_workflow_create_invoice_filter'
    )
    create_invoice_filter.domain = (
        "[('state', 'in', ['sale', 'done', 'waiting_calculator']), "
        "('invoice_status', '=', 'to invoice'), "
        "('partner_company_type', '=', 'agency_customer'), "
        "('order_line.qty_to_invoice', '>', 0)]")

    validate_invoice_filter = ctx.env.ref(
        'sale_automatic_workflow.automatic_workflow_validate_invoice_filter'
    )
    validate_invoice_filter.domain = (
        "[('state', 'in', ['draft']), "
        "('partner_company_type', '=', 'agency_customer')]")


@anthem.log
def main(ctx):
    """ Main: sale workflow settings """
    sale_workflow_configuration(ctx)
