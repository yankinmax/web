# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class CrmActivity(models.Model):
    _inherit = 'crm.activity'

    action_hour = fields.Float(
        string='Action hour',
        digits=(16, 2),
    )
