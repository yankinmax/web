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
        'base',
        'specific_base',
        'sale',
    ],
    'data': [
        'data/depiltech_payment_mode.xml',
        'security/ir.model.access.csv',
        'report/sale_order.xml',
        'views/depiltech_payment_mode.xml',
        'views/sale_order.xml'
    ],
    'installable': True,
    'auto_install': False,
}
