# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def _get_default_bounce_address(self):
        self_c = self.with_context(
            catchall_company_id=self.env.user.company_id.id
        )
        return super(IrMailServer, self_c)._get_default_bounce_address()
