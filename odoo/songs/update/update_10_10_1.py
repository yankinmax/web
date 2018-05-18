# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
from anthem.lyrics.modules import update_translations, uninstall


@anthem.log
def remove_manual_views(ctx):
    """ Remove manual views of delivery slip report"""
    view_names = [
        'report_delivery_document_specific_manually',
        'report_delivery_document_inherit_sale_stock_manually',
        'report.invoice.inherit.sale.manually',
        'report_purchaseorder_document_specific_manually',
        'report_saleorder_document_specific_manually',
        'report_sale_order_specific_specific_manually',
        'stock.picking.internal.search.manually',
        'stock.history.search.specific.manually',
        'account.invoice.supplier.form.specific.manually',
    ]
    ctx.env['ir.ui.view'].with_context(active_test=False).search(
        [('name', 'in', view_names)]).unlink()


@anthem.log
def uninstall_module(ctx):
    """Uninstall module 'base_dj'"""
    uninstall(ctx, ['base_dj'])


@anthem.log
def pre(ctx):
    """ Applying update 10.10.1 """
    remove_manual_views(ctx)
    uninstall_module(ctx)


@anthem.log
def post(ctx):
    """ Applying update 10.10.1 """
    update_translations(ctx, ['mtsmte_reports'])
