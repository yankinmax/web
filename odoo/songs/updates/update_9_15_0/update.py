# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from anthem.lyrics.records import create_or_update

import anthem


@anthem.log
def update_res_partner_rules(ctx):
    """ Update rules for res partner """

    group_dt_compta = ctx.env.ref('scenario.grp_dt_compta')

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
    """ Update 9.15.0 """
    update_res_partner_rules(ctx)
