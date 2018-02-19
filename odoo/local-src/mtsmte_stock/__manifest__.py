# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MTS-MTE Specific Stock module",
    "version": "10.0.1.0.0",
    "description": """Specific stock module

    fixes scraping of the products in a stock picking""",
    "depends": [
        'stock',
        'sale',
        'sale_stock',
        'mtsmte_sale',
    ],
    "author": "Camptocamp",
    "website": "http://www.camptocamp.com",
    "license": "AGPL-3",
    "category": "Warehouse",
    "data": [
        'views/stock_scrap_views.xml'
    ],
    'installable': True,
}
