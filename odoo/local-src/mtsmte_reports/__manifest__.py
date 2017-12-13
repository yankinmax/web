# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'MTS MTE Reports',
    'description': 'Specific reports customization',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Reporting',
    'depends': [
        'report',
        'report_py3o',
        'project',
        'sale',
        'sale_order_dates',
        'purchase',
    ],
    'website': 'https://www.camptocamp.com',
    'data': [
        'data/py3o_server.xml',
        'reports/assets.xml',
        'reports/layouts.xml',
        'reports/reports.xml',
        'reports/reports_py3o.xml',
        'data/email_template.xml',
        'reports/project_analysis.xml',
        'reports/purchase_order.xml',
        'reports/purchase_quotation.xml',
        'reports/sale.xml',
        'reports/invoice_report.xml',
        'wizards/project_analysis_wiz.xml',
        'views/company.xml',
        'views/project.xml',
    ],
    'installable': True,
}
