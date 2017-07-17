# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def create_journal_ir_property(ctx):
    automatic_workflow = ctx.env.ref(
        'sale_automatic_workflow.automatic_validation')

    companies = ctx.env['res.company'].search([])
    admin_company = ctx.env.user.company_id
    for company in companies:
        ctx.env.user.company_id = company
        sale_journal = ctx.env['account.journal'].search([
            ('company_id', '=', company.id), ('type', '=', 'sale')])
        if sale_journal and len(sale_journal) == 1:
            automatic_workflow.property_journal_id = sale_journal.id

    ctx.env.user.company_id = admin_company


@anthem.log
def validate_order(ctx):
    automatic_workflow = ctx.env.ref(
        'sale_automatic_workflow.automatic_validation')
    automatic_workflow.validate_order = False


@anthem.log
def main(ctx):
    """ Main: sale workflow settings """
    validate_order(ctx)
    create_journal_ir_property(ctx)
