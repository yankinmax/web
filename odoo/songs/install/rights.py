# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import anthem


@anthem.log
def add_groups_to_admin_user(ctx):
    """ add_groups_to_admin_user """
    ctx.env.user.company_ids = ctx.env.ref('base.main_company').ids
    groups = [
        ctx.env.ref('account.group_account_manager'),
        ctx.env.ref('purchase.group_purchase_manager'),
        ctx.env.ref('sales_team.group_sale_manager'),
        ctx.env.ref('sales_team.group_sale_salesman'),
        ctx.env.ref('sales_team.group_sale_salesman_all_leads'),
        ctx.env.ref('base.group_no_one'),
        ctx.env.ref('base.group_multi_currency'),
        ctx.env.ref('base.group_multi_company'),
    ]
    for group in groups:
        group.write({
            'users': [(4, ctx.env.user.id)]
        })


@anthem.log
def setup_export_rights(ctx):
    """ disable export for all object

    Export is allowed for Export group only, this is defined in
    module specific_security
    """
    export_group = ctx.env.ref('specific_security.group_export')
    # group_id is a m2m
    domain = [('group_id', 'not in', [export_group.id])]
    model_accesses = ctx.env['ir.model.access'].search(domain)
    model_accesses.write({'perm_export': False})


@anthem.log
def main(ctx):
    add_groups_to_admin_user(ctx)
    setup_export_rights(ctx)
