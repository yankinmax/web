# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'DepilTech Specific base',
 'description': "",
 'version': '10.0.1.0.0',
 'author': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Others',
 'depends': ['mail',
             'sale',
             'account',
             'partner_survey',
             'partner_firstname',
             'product',
             'l10n_fr_siret',
             'crm',
             'utm',
             'sale_crm',
             'sale_stock',
             'sales_team',
             'stock',
             'survey',
             'specific_security',
             ],
 'website': 'http://www.camptocamp.com',
 'data': [
     # Security
     'security/ir.model.access.csv',
     # Wizard
     'wizard/crm_opportunity_to_customer.xml',  # Need to load before views
     # Views
     'views/actions.xml',
     'views/menus.xml',
     'views/res_company.xml',
     'views/company_phototherapist.xml',
     'views/company_schedule.xml',
     'views/res_partner.xml',
     'views/survey_templates.xml',
     'views/sale_order.xml',
     'views/account_invoice.xml',
     'views/pricelist.xml',
     'views/res_users.xml',
     'views/crm_lead.xml',
     'views/crm_stage.xml',
     'views/utm.xml',
     'views/res_country.xml',
     'views/account_payment.xml',
     'views/sale_config.xml',
     # Data
     'data/ir_rule.xml',
     'data/ir_property.xml',
     'data/base_override.yml',
     'data/ir_actions_server.xml',
     'data/base_action_rule.xml',
     'data/ir_config_parameter.xml',
     'data/decimal_precision.xml',
     # Report
     'report/sale_order.xml',
 ],
 'installable': True,
 }
