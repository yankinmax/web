# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class MailCatchallDomain(models.Model):
    _name = 'mail.catchall.domain'

    name = fields.Char(string='Domain', required=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
    )

    _sql_constraints = [
        ('company_uniq',
         'unique (company_id)',
         'Only one domain per company is allowed.')
    ]
