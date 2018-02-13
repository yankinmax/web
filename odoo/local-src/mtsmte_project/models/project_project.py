# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    report_number = fields.Char(
        string='Report number',
    )

    date_send_pdf = fields.Date(
        string='PDF report send date',
    )

    date_shipping = fields.Date(
        string='Shipping date',
    )

    samples_joined = fields.Char(
        string='Samples joined to Shipping',
    )

    shipping_mode = fields.Char(
        string='Shipping mode',
    )

    precious_substance = fields.Char(
        string='Precious substance',
    )

    invoice_sent = fields.Char(
        string='Invoice sent',
    )

    remark = fields.Text(
        string='Remarks',
    )
