# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def remove_bad_report_invoice_b2b(ctx):
    qweb_view = ctx.env['ir.ui.view'].search([
        ('name', '=', 'report_invoice_document'),
        ('key', '=', False),
        ('type', '=', 'qweb'),
    ])
    if qweb_view:
        qweb_view.unlink()


@anthem.log
def main(ctx):
    """ Main: pre update 10.1.1 """
    remove_bad_report_invoice_b2b(ctx)
