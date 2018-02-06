# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MTS-MTE Specific Sale module",
    "version": "10.0.1.0.0",
    "depends": [
        'sale',
        'sale_stock',
        'sale_order_dates',
        'project',
        'sale_timesheet',
        'account',
        'maintenance',
        'sale_project_fixed_price_task_completed_invoicing',
        # fix for warning in onchange BSMTS-254
        'website_quote',
    ],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://www.camptocamp.com",
    "license": "AGPL-3",
    "category": "Sale",
    "data": [
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'wizards/so_sync_task.xml',
        'views/sale_order_views.xml',
        'views/project_views.xml',
        'views/product_views.xml',
        'views/project_task_views.xml',
        'views/substance_views.xml',
        'views/invoice_views.xml',
        'views/product_categ.xml',
        'views/product_method.xml',
        'views/product_extraction_type.xml',
        'views/substance_measure.xml',
        'views/result_sentence.xml',
        'views/task_stage.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
}
