# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def change_voucher_code_from_sequence(ctx):
    Program = ctx.env['sale.discount.program']
    programs = Program.search([('voucher_code', '=like', 'VOU%'),
                               ('used', '!=', True)])
    for prog in programs:
        prog.voucher_code = Program.with_context(
            program_voucher=True)._default_voucher_code()


@anthem.log
def remove_discount_program_sequence(ctx):
    seq = ctx.env.ref(
        'sale_discount_program.seq_sale_discount_program_voucher')
    if seq:
        seq.unlink()


@anthem.log
def main(ctx):
    """ Main: post update 10.1.0 """
    change_voucher_code_from_sequence(ctx)
    remove_discount_program_sequence(ctx)
