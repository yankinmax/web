# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, exceptions, models
from odoo.tools import ormcache


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def get_param(self, key, default=False):
        if key == 'mail.catchall.domain':
            ctx = self.env.context
            model = ctx.get('catchall_model') or ctx.get('default_model')
            res_id = ctx.get('catchall_res_id') or ctx.get('default_res_id')
            company_id = None
            if model and res_id:
                record = self.env[model].browse(res_id)
                if 'company_id' in record._fields:
                    company_id = record.company_id.id
            if not company_id:
                company_id = (ctx.get('catchall_company_id') or
                              ctx.get('company_id'))
            if not company_id:
                company_id = self.env.user.company_id.id
            return self._get_param_company(key, company_id) or default
        else:
            _super = super(IrConfigParameter, self)
            return _super.get_param(key, default=default)

    @api.model
    @ormcache('self._uid', 'key', 'company_id')
    def _get_param_company(self, key, company_id):
        return self.env['mail.catchall.domain'].search(
            [('company_id', '=', company_id)]
        ).name or None

    @api.model
    def set_param(self, key, value, groups=()):
        if key == 'mail.catchall.domain':
            if groups:
                raise exceptions.UserError(
                    _('Not possible to set a group on mail.catchall.domain')
                )
            self._get_param.clear_cache(self)
            company_id = self.env.user.company_id.id
            param = self.env['mail.catchall.domain'].search(
                [('company_id', '=', company_id)]
            )
            if param:
                old = param.name
                if value is not False and value is not None:
                    param.name = value
                else:
                    param.unlink()
                return old
            else:
                self.env['mail.catchall.domain'].create({
                    'name': value,
                    'company_id': company_id
                })
                return False
        else:
            _super = super(IrConfigParameter, self)
            return _super.set_param(key, value, groups=groups)
