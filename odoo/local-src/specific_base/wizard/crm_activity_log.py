# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytz

from datetime import timedelta

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

        if self.next_activity_id.action_hour:
            tz_name = self.env.context.get('tz') or self.env.user.tz
            context_tz = pytz.timezone(tz_name)

            timestamp = (
                fields.Datetime.from_string(self.date_action) +
                timedelta(hours=self.next_activity_id.action_hour)
            )
            tz_timestamp = context_tz.localize(timestamp)
            utc_timestamp = tz_timestamp.astimezone(pytz.utc)

            self.datetime_action = fields.Datetime.to_string(utc_timestamp)
        else:
            self.datetime_action = self.date_action

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
