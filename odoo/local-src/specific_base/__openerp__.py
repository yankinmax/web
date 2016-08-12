# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'DepilTech Specific base',
 'description': "",
 'version': '1.0',
 'author': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Others',
 'depends': ['mail',
             'sale',
             'account',
             'partner_survey',
             'partner_firstname',
             'l10n_fr_siret',
             'crm',
             'utm',
             'sale_crm',
             ],
 'website': 'http://www.camptocamp.com',
 'data': ['views/res_company.xml',
          'views/company_phototherapist.xml',
          'views/company_schedule.xml',
          'views/res_partner.xml',
          'views/survey_templates.xml',
          'views/sale_order.xml',
          ],
 'installable': True,
 }
