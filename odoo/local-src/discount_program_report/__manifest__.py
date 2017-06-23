# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Depil Tech - Discount Program Report',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Others',
    'depends': [
        'specific_discount_program',
        'report'
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Data
        'data/program_report.xml',
        'data/program_mail_template.xml',
        'data/program_report_templates.xml',
        # Views
        'views/program.xml',
        'views/report_config.xml',
    ],
    'installable': True,
}
