# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MTS-MTE Specific Sale module",
    "version": "10.0.1.0.0",
    "depends": [
        'sale',
        'project',
        'sale_timesheet',
        'account',
        'maintenance',
    ],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://www.camptocamp.com",
    "license": "AGPL-3",
    "category": "Sale",
    "data": [
        'views/sale_order_views.xml',
        'views/project_views.xml',
        'views/product_views.xml',
        'views/project_task_views.xml',
        'views/substance_views.xml',
        'views/invoice_views.xml',
        'views/menu_items.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
