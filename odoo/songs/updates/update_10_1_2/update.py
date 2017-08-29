# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def clean_groups(ctx):
    """ Clean useless groups """

    bad_siege_group = ctx.env.ref('specific_base.group_siege_depiltech',
                                  raise_if_not_found=False)
    if bad_siege_group:
        bad_siege_group.unlink()

    bad_admin_group = ctx.env.ref('specific_base.group_admin_depiltech',
                                  raise_if_not_found=False)
    if bad_admin_group:
        bad_admin_group.unlink()


@anthem.log
def update_crm_stage_values(ctx):
    """ Define 'Used when convert to customer' value on crm stage """
    won_stage = ctx.env.ref('crm.stage_lead4')
    if won_stage:
        won_stage.used_when_convert_to_customer = True


@anthem.log
def update_vouchers(ctx):

    vouchers = ctx.env['sale.discount.program'].search([
        ('voucher_code', '!=', False)])
    gift = vouchers.filtered(lambda v: not v.partner_id)
    vouchers -= gift
    gift.write({
        'type': 'gift_voucher'
    })
    vouchers.write({
        'type': 'voucher'
    })


@anthem.log
def update_promo_codes(ctx):

    promo_codes = ctx.env['sale.discount.program'].search([('promo_code', '!=', False)])
    promo_codes.write({
        'type': 'promo_code'
    })


@anthem.log
def update_discount_programs(ctx):

    programs = ctx.env['sale.discount.program'].search([
        ('automatic', '=', True)])
    programs.write({
        'type': 'discount_program'
    })


@anthem.log
def main(ctx):
    """ Main: update 10.1.2 """
    clean_groups(ctx)
    update_crm_stage_values(ctx)
    update_discount_programs(ctx)
    update_promo_codes(ctx)
    update_vouchers(ctx)
