# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    used_when_convert_to_customer = fields.Boolean(
        string='Used when convert to customer',
    )
