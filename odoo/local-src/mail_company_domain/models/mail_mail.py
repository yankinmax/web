# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class MailMail(models.Model):
    _inherit = 'mail.mail'

    def send(self, auto_commit=False, raise_exception=False):
        for mail in self:
            model_name = mail.model
            res_id = mail.res_id
            if model_name and res_id:
                mail_c = mail.with_context(catchall_model=model_name,
                                           catchall_res_id=res_id)
            elif mail.company_id:
                mail_c = mail.with_context(
                    catchall_company_id=mail.company_id.id
                )
            else:
                mail_c = mail
            super(MailMail, mail_c).send(auto_commit=auto_commit,
                                         raise_exception=raise_exception)

        return True
