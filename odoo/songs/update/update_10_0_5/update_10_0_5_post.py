# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def journal_cancel(ctx):
    """ Allow canceling entries on journal """
    journals = ctx.env['account.journal'].search([])
    for journal in journals:
        journal.write({'update_posted': True})


@anthem.log
def main(ctx):
    journal_cancel(ctx)
