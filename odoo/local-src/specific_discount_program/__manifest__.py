# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Depil Tech - Promotions',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Others',
    'depends': [
        'specific_base',
        'sale_discount_program'
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Data
        'data/ir_config_parameter.xml',
        'data/product.xml',
        'data/product.pricelist.csv',
        'data/product.pricelist.item.csv',
        # Report
        'report/account_invoice.xml',
        # Security
        'security/ir.model.access.csv',
        'security/program.xml',
        # Views
        'views/account_invoice.xml',
        'views/program.xml',
        'views/program_action.xml',
        'views/product_template.xml',
        'views/res_config.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
}
