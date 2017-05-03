# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'MTS MTE Reports',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Reporting',
    'depends': [
        'report_py3o',
        'project',
    ],
    'website': 'https://www.camptocamp.com',
    'data': [
        'data/py3o_server.xml',
        'views/company.xml',
        'reports/reports.xml',
        'reports/layouts.xml',
    ],
    'installable': True,
}
