# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'Report Page EndNote',
 'summary': "Add a page to any report with content (HTML) "
            "taken from an Odoo object",
 'version': '1.0',
 'author': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Others',
 'depends': ['report',
             'base_report_auto_create_qweb',
             ],
 'website': 'http://www.camptocamp.com',
 'data': ['security/ir.model.access.csv',
          'views/report_page_endnote.xml',
          'report/report_page_endnote.xml',
          ],
 'installable': True,
 }
