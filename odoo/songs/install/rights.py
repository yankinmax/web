# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from anthem.lyrics.records import create_or_update

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
def update_res_partner_rules(ctx):
    """ Update rules for res partner """

    group_dt_compta = ctx.env.ref('specific_security.grp_dt_compta')

    # Update the default rule
    res_partner_rule = ctx.env.ref('base.res_partner_rule')
    res_partner_rule.write({
        'groups': [(5, 0, 0)],
        'domain_force': "[(1, '=', 1)]",
        'active': True,
    })

    # Create a specific rule for DT accounting group
    create_or_update(
        ctx,
        'ir.rule',
        'scenario.res_partner_rule_dt_accounting_group',
        {
            'name': 'res.partner for "DT accounting group"',
            'model_id': ctx.env.ref('base.model_res_partner').id,
            'perm_read': True,
            'perm_create': True,
            'perm_write': True,
            'perm_unlink': True,
            'domain_force': "[(1, '=', 1)]",
            'groups': [(6, 0, [group_dt_compta.id])],
        }
    )

    # Create a specific rule for base group user
    create_or_update(
        ctx,
        'ir.rule',
        'scenario.res_partner_rule_base_group_user',
        {
            'name': 'res.partner for base group user',
            'model_id': ctx.env.ref('base.model_res_partner').id,
            'perm_read': True,
            'perm_create': True,
            'perm_write': True,
            'perm_unlink': True,
            'domain_force': "['|',"
                            "('company_id','child_of',[user.company_id.id]),"
                            "('company_id','=',False)]",
            'groups': [(6, 0, [ctx.env.ref('base.group_user').id])],
        }
    )


@anthem.log
def main(ctx):
    add_groups_to_admin_user(ctx)
    update_res_partner_rules(ctx)
