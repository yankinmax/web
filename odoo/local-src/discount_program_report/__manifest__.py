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
        'report',
        'mail',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Data
        'data/report_data.xml',
        'data/report_config_data.xml',
        'data/ir_cron_data.xml',
        # Report
        'report/program_mail_template.xml',
        'report/program_report_templates.xml',
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/program.xml',
        'views/report_config.xml',
    ],
    'installable': True,
}
