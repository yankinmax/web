# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{'name': 'DepilTech specific security for export',
 'description': "Security management",
 'version': '10.0.1.0.0',
 'author': 'Camptocamp',
 'license': 'LGPL-3',
 'category': 'Others',
 'depends': [
     'base_export_manager',
     'specific_security',
     'account_banking_pain_base',
     'account_fiscal_year',
     'account_online_sync',
     'account_payment_order',
     'account_payment_sale',
     'account_reports',
     'account',
     'analytic',
     'attachment_s3',
     'auth_oauth',
     'barcodes',
     'base_action_rule',
     'base_import',
     'base',
     'board',
     'bus',
     'calendar',
     'crm_phone',
     'crm',
     'date_range',
     'decimal_precision',
     'fetchmail',
     'fields_regex_validation',
     'inter_company_rules',
     'mail_push',
     'mail',
     'marketing_campaign',
     'partner_changeset',
     'partner_survey',
     'payment',
     'procurement_jit',
     'procurement',
     'product',
     'purchase',
     'report_page_endnote',
     'report',
     'resource',
     'sale_automatic_workflow',
     'sale_discount_program',
     'sale_stock',
     'sale',
     'specific_base',
     'specific_discount_program',
     'specific_payment_mode',
     'stock_account',
     'stock',
     'subscription',
     'survey',
     'web_editor',
     'web_tour',
     'website',
     ],
 'website': 'http://www.camptocamp.com',
 'data': ['security/ir.model.access.csv',
          ],
 'installable': True,
 }
