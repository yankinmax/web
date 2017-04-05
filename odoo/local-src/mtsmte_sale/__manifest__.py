# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MTS-MTE Specific Sale module",
    "version": "10.0.1.0.0",
    "depends": [
        'sale',
        'project',
    ],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://www.camptocamp.com",
    "license": "GPL-3",
    "category": "Sale",
    "data": [
        'views/sale_order.xml',
        'views/project.xml',
        # 'data/res_groups_data.xml',
    ],
    'installable': True,
}
