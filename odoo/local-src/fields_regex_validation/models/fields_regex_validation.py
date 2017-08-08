# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import uuid
from psycopg2 import IntegrityError, ProgrammingError
import odoo
from odoo import models, fields, api, _
from odoo.modules.registry import RegistryManager


class FieldsRegexValidation(models.Model):
    _name = 'fields.regex.validation'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    regex = fields.Char(string="Validation Regular Expression",
                        required=True)
    model_id = fields.Many2one(comodel_name='ir.model', string="Object",
                               required=True)
    model_name = fields.Char(related='model_id.model', readonly=True)
    field_id = fields.Many2one(comodel_name='ir.model.fields', string="Field",
                               required=True)
    field_name = fields.Char(related='field_id.name', readonly=True)
    error_msg = fields.Text(required=True, translate=True)
    constraint_name = fields.Char()

    def __init__(self, pool, cr):
        super(FieldsRegexValidation, self).__init__(pool, cr)

        cr.execute("select id from ir_module_module where "
                   "name='fields_regex_validation' and state='installed';")
        res = cr.dictfetchall()
        if res:
            query = "select * from fields_regex_validation where active;"
            cr.execute(query)
            for res in cr.dictfetchall():
                self._update_sql_error_dict(res['constraint_name'],
                                            res["error_msg"], pool=pool)

    def _update_sql_error_dict(self, constraint_name, error_msg, pool=None):
        if not pool:
            pool = self.pool
        pool._sql_error.update({constraint_name.encode('utf-8'):
                                error_msg.encode('utf-8')})

    @api.onchange('model_id')
    def onchange_model_id(self):
        model = self.model_id.model
        return {'domain': {'field_id': [('model', '=', model)]}}

    @api.multi
    def drop_constraint(self):
        self.ensure_one()
        query = """
            ALTER TABLE %(table)s
            DROP CONSTRAINT %(constraint_name)s;
            """ % {'table': self.env[self.model_name]._table,
                   'constraint_name': self.constraint_name}
        try:
            self.env.cr.execute(query)
        except ProgrammingError as e:
            if "does not exist" in e.args[0]:
                pass
            else:
                raise

        return True

    @api.model
    def create_constraint(self, constraint_name, model, field_name, regex):
        query = """
        ALTER TABLE %(table)s
        ADD CONSTRAINT %(constraint_name)s
        CHECK (%(field_name)s is null or %(field_name)s ~* '%(regex)s');
        """ % {'table': self.env[model]._table,
               'constraint_name': str(constraint_name),
               'field_name': field_name,
               'regex': regex}
        try:
            self.env.cr.execute(query)
        except IntegrityError as ex:
            error = """
Cannot apply this constraint because some records don't satisfy it.

Please correct your data first.

Detailled error: %r"""
            raise IntegrityError(_(error) % ex.args[0])

        return True

    @api.model
    def create(self, values):
        """
        """
        model_name = self.env['ir.model'].browse(values['model_id']).model
        field_name = self.env['ir.model.fields'].browse(
            values['field_id']).name
        constraint_name = uuid.uuid4().hex
        if not values.get('constraint_name', False):
            values['constraint_name'] = 'c_'+constraint_name

        self.create_constraint('c_'+constraint_name,
                               model_name,
                               field_name,
                               values.get('regex'))

        # signal changes to registry to the others (eventual) workers
        # be aware of this new constraint
        if not odoo.multi_process:
            self._update_sql_error_dict(constraint_name, values['error_msg'])
        else:
            RegistryManager.signal_registry_change(self.env.cr.dbname)

        return super(FieldsRegexValidation, self).create(values)

    @api.multi
    def write(self, values):
        """
        """
        for rec in self:
            if ('model_id' in values or
                    'field_id' in values or
                    'regex' in values or
                    'active' in values):

                # first drop constraint
                rec.drop_constraint()
                constraint_name = uuid.uuid4().hex
                values['constraint_name'] = 'c_'+constraint_name

                super(FieldsRegexValidation, rec).write(values)
                # then try to recreate the modified one
                rec.create_constraint(rec.constraint_name,
                                      rec.model_name,
                                      rec.field_name,
                                      rec.regex)
            else:
                super(FieldsRegexValidation, rec).write(values)

        # signal changes to registry to the others (eventual) workers
        # be aware of this new constraint
        if not odoo.multi_process:
            for rec in self:
                self._update_sql_error_dict(rec.constraint_name, rec.error_msg)
        else:
            RegistryManager.signal_registry_change(self.env.cr.dbname)

        return True

    @api.multi
    def unlink(self):
        """
        """
        for rec in self:
            rec.drop_constraint()

        super(FieldsRegexValidation, self).unlink()
        # signal changes to registry to the others (eventual) workers
        # be aware of this new constraint
        if not odoo.multi_process:
            for rec in self:
                del self.pool._sql_error[rec.constraint_name]
        else:
            RegistryManager.signal_registry_change(self.env.cr.dbname)
        return True
