# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Depil Tech Account Customization',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Specific',
    'website': 'http://www.camptocamp.com',
    'images': [],
    'depends': [
        'base',
        'account',
        # TODO: The module 'account_tax_exigible' disapeared in V10.
        # TODO: Check if this content added in another module ?
        # TODO: To check all are OK, look the trello card 216:
        # 'account_tax_exigible',
    ],
    'data': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
