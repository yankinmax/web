# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ...install.rights import setup_export_rights


@anthem.log
def move_groups(ctx):
    """ Moving groups to specific_base"""
    ctx.env.cr.execute("""
        UPDATE ir_model_data SET module = 'specific_security'
        WHERE module = 'scenario'
        AND model = 'res.groups';
    """)


@anthem.log
def move_rules(ctx):
    """ Moving rules to specific_security"""
    ctx.env.cr.execute("""
        UPDATE ir_model_data SET module = 'specific_base'
        WHERE module = 'scenario'
        AND model = 'ir.rule';
    """)


def move_pricelists(ctx):
    """ Moving pricelists to specific_discount_program"""
    ctx.env.cr.execute("""
        UPDATE ir_model_data SET module = 'specific_discount_program'
        WHERE module = 'scenario'
        AND model = 'product.pricelist';
    """)
    ctx.env.cr.execute("""
        UPDATE ir_model_data SET module = 'specific_discount_program'
        WHERE module = 'scenario'
        AND model = 'product.pricelist.item';
    """)


# Don't execute this script before install of specific_security module
@anthem.log
def unlink_depiltech_payment_modes(ctx):
    """ Unlink all existing depiltech payment modes"""
    ctx.env['depiltech.payment.mode'].search([]).unlink()


@anthem.log
def main(ctx):
    """ Main: update 10.1.0 """
    move_groups(ctx)
    move_rules(ctx)
    move_pricelists(ctx)
    setup_export_rights(ctx)
