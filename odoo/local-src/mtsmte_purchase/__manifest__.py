# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MTSMTE Specific Purchase Module",
    "version": "10.0.1.0.0",
    "description": """Specific module for MTSMTE.

    if invoice name is empty -> copy reference.
    in purchase order origin is invisible.
    """,
    "depends": [
        'purchase',
        'account',
    ],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://www.camptocamp.com",
    "license": "AGPL-3",
    "category": "Purchase",
    "data": [
        'views/purchase_views.xml',
        'views/account_invoice.xml',
    ],
    'installable': True,
}
