# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'DepilTech specific security',
 'description': "Security management",
 'version': '10.0.1.0.0',
 'author': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Others',
 'depends': ['sale',
             'account',
             'purchase',
             'marketing_campaign',
             'account_payment_order',
             ],
 'website': 'http://www.camptocamp.com',
 'data': ['security/groups.xml',
          'security/res.groups.csv',
          'views/sale_order.xml',
          'views/account_invoice.xml',
          ],
 'installable': True,
 }
