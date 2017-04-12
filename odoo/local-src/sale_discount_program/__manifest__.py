# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Discount Programs',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Others',
    'depends': [
        'sale',
        'sale_stock',
        # TODO: remove if OCA
        'specific_base',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        'data/product_voucher.xml',
        'data/program_sequence.xml',
        'security/ir.model.access.csv',
        'views/program.xml',
        'views/program_action.xml',
        'views/program_condition.xml',
        'views/res_config.xml',
        'views/sale.xml',
    ],
    'installable': True,
}
