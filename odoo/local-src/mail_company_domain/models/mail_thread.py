# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def get_empty_list_help(self, help):
        model = self.env.context.get('empty_list_help_model')
        res_id = self.env.context.get('empty_list_help_id')
        if model and res_id:
            self_c = self.with_context(catchall_model=model,
                                       catchall_res_id=res_id)
            return super(MailThread, self_c).get_empty_list_help(help)
        return super(MailThread, self).get_empty_list_help(help)

    @api.model
    def message_get_reply_to(self, res_ids, default=None):
        result = dict.fromkeys(res_ids, False)
        model_name = self.env.context.get('thread_model') or self._name
        for res_id in res_ids:
            self_c = self.with_context(catchall_model=model_name,
                                       catchall_res_id=res_id)
            res = super(MailThread, self_c).message_get_reply_to(
                [res_id], default=default
            )
            result.update(res)
        return result
