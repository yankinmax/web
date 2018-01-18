# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MTS-MTE Specific accounting module",
    "version": "10.0.1.0.0",
    "depends": [
        'account_reports_followup',
        'board',
        'account_due_list',
        'l10n_ch_pain_credit_transfer',
        'account_payment_order'
    ],
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://www.camptocamp.com",
    "license": "AGPL-3",
    "category": "Account",
    "data": [
        "views/management_dashboard.xml",
    ],
    'installable': True,
}
