# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Depil Tech - Promotions',
    'version': '9.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Others',
    'depends': [
        'specific_base',
        'sale_discount_program'
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        'security/ir.model.access.csv',
        'security/program.xml',
        'views/program.xml',
        'views/res_config.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
}
