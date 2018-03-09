# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    report_number = fields.Char(
        related="project_project_id.report_number",
        store=True,
    )
