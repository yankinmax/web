# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def move_groups(ctx):
    """ Moving groups to specific_base"""
    ctx.env.cr.execute("""
        UPDATE ir_model_data SET module = 'specific_base'
        WHERE module = 'scenario'
        AND model = 'res.groups';
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


@anthem.log
def main(ctx):
    """ Main: update 10.1.0 """
    move_groups(ctx)
    move_pricelists(ctx)
