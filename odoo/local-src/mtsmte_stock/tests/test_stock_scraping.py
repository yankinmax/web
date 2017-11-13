# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import odoo.tests.common as common

# TODO
# The test doesn't work as i couldn't replicate the workflow fully
# During the confirmation of sale.order it is supposed to create
# 6 stock.pickings but i was always getting one. I found that it
# depends on the stock.location.route inside the product. Even though i tried
# selecting one, and even creating copy of the one that works from the UI
# and is created via song -> still resulted in only 1 picking


class TestStockScraping(common.TransactionCase):

    def _create_route(self):
        self.route = self.env["stock.location.route"].create({
            "active": True,
            "categ_ids": "",
            "company_id": self.env.ref("base.main_company").id,
            "name": "MTO: Dur. + Pol.",
            "product_categ_selectable": False,
            "product_selectable": True,
            "push_ids": "",
            "sale_selectable": False,
            "sequence": 0,
            "supplied_wh_id": "",
            "supplier_wh_id": "",
            "warehouse_ids": "",
            "warehouse_selectable": False,
        })

    def _create_sale_order(self):
        self._create_route()
        self.product.route_ids = [(4, self.route.id)]
        vals_order_line = {
            "product_id": self.product.id,
            "product_uom_qty": 100,
        }
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            "picking_policy": "direct",
            'order_line': [(0, 0, vals_order_line)],
            'pricelist_id': self.env.ref('product.list0').id,
        })
        return sale_order

    def setUp(self):
        super(TestStockScraping, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_16')
        self.sale_order1 = self._create_sale_order()

    def test_stock_scraping(self):
        self.sale_order1.action_confirm()
        pickings = self.sale_order1.picking_ids
        self.assertEquals(len(pickings), 6)
