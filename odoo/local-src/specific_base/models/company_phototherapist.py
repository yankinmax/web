# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompanyPhototherapist(models.Model):
    _name = 'res.company.phototherapist'
    _desc = "Manage phototherapist of a company"

    company_id = fields.Many2one(comodel_name='res.company')
    active = fields.Boolean(default=True)
    name = fields.Char()
    date_deleted = fields.Date()
