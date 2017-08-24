# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Depil Tech - Payment mode',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Specific',
    'website': 'http://www.camptocamp.com',
    'depends': [
        'account_payment_sale',
        'account_payment_term_extension',
        'account_payment_mode',
        'sale',
        'specific_base',
        'specific_discount_program',
    ],
    'data': [
        # Data
        'data/depiltech_payment_mode.xml',  # Need to load this file first
        'data/account_payment_method.xml',
        'data/ir_config_parameter.xml',
        # Security
        'security/ir.model.access.csv',
        # Report
        'report/sale_order.xml',
        # Views
        'wizard/account_payment_mode_generator.xml',
        'views/account_payment_method.xml',
        'views/account_payment_mode.xml',
        'views/depiltech_payment_mode.xml',
        'views/sale_config.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
}
