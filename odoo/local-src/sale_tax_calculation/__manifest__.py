# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Tax Calculation',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Specific',
    'website': 'http://www.camptocamp.com',
    'depends': [
        'account',
        'sale',
        # TODO: remove if OCA
        'specific_base',
    ],
    'data': [
    ],
    'installable': True,
    'auto_install': False,
}
