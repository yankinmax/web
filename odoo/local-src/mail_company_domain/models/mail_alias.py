# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class MailAlias(models.Model):
    _inherit = 'mail.alias'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
    )

    @api.multi
    def _get_alias_domain(self):
        for record in self:
            rec = record.with_context(
                catchall_model=self._name,
                catchall_res_id=record.id,
            )
            super(MailAlias, rec)._get_alias_domain()
            record.alias_domain = rec.alias_domain
