# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class Program(models.Model):
    _name = 'sale.discount.program'

    name = fields.Char('Name')

    condition_ids = fields.One2many(
        comodel_name='sale.discount.program.condition',
        inverse_name='program_id',
    )

    action_ids = fields.One2many(
        comodel_name='sale.discount.program.action',
        inverse_name='program_id',
    )

    @api.multi
    def is_valid(self, sale):
        self.ensure_one()
        if not self.condition_ids:
            # TODO: no condition
            raise NotImplementedError()

        # TODO: and / or
        return any(condition.check(sale) for condition in self.condition_ids)

    @api.multi
    def apply_actions(self, sale):
        self.ensure_one()

        for action in self.action_ids:
            action.apply(sale)

    @api.multi
    def apply_for_sale(self, sale):
        """ Apply this action on sale.order *sale*.
        """
        for program in self:
            if program.is_valid(sale):
                program.apply_actions(sale)
