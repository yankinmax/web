# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    # To know what was the company when the message has been created.
    # It's used by MailMail.send to know which domain alias choose when
    # there is no model/res_id on the message
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
    )
