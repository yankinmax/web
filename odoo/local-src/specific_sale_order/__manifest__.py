# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Depil Tech - Specific Sale Order',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Others',
    'depends': [
        'sale',
        'specific_base',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        'report/sale_order_template.xml',
        'security/groups.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
}
