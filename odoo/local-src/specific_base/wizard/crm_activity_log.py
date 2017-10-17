# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class CrmActivityLog(models.TransientModel):
    _inherit = 'crm.activity.log'

    datetime_action = fields.Datetime(
        string='Next Activity Date',
    )

    @api.onchange('datetime_action')
    def onchange_datetime_action(self):
        self.date_action = self.datetime_action

    @api.onchange('next_activity_id')
    def onchange_next_activity_id(self):
        super(CrmActivityLog, self).onchange_next_activity_id()

        lead_model = self.env['crm.lead']
        self.datetime_action = lead_model.get_datetime_action_in_timestamp(
            self.date_action,
            self.next_activity_id.action_hour
        )

    @api.multi
    def action_log(self):
        result = super(CrmActivityLog, self).action_log()
        self.mapped('lead_id').write({
            'datetime_action': False,
        })
        return result

    @api.multi
    def action_schedule(self):
        result = super(CrmActivityLog, self).action_schedule()
        for log in self:
            log.lead_id.write({
                'datetime_action': log.datetime_action,
            })
        return result

    @api.model
    def create(self, values):
        if values.get('datetime_action'):
            values['date_action'] = values['datetime_action']
        return super(CrmActivityLog, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('datetime_action'):
            values['date_action'] = values['datetime_action']
        return super(CrmActivityLog, self).write(values)
