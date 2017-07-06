# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class ProgramCondition(models.Model):
    _inherit = 'sale.discount.program.condition'

    type_condition = fields.Selection(
        selection_add=[
            ('customer_sponsor', 'Sponsorship'),
            ('another_order_validated', 'Another order validated'),
        ]
    )

    sale_order_validated_since = fields.Integer()
    sale_order_validated_until = fields.Integer()

    @api.multi
    def _check_customer_sponsor(self, sale):
        """ Check if the sale order customer has a sponsor and if it's his
        first sale.order
        """
        return sale.partner_id.sponsor_id \
            and not sale.partner_id.already_bought

    @api.multi
    def _get_another_order_validated_name(self):
        self.ensure_one()
        return _(
            "Another order validated between %s and %s days"
        ) % (
            (self.sale_order_validated_since or 0),
            (self.sale_order_validated_until or 0)
        )

    def get_another_order_validated(self, sale):
        max_confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(
                days=self.sale_order_validated_since
            )
        )
        min_confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(
                days=self.sale_order_validated_until
            )
        )
        last_validated_order_order = self.env['sale.order'].search(
            [
                ('partner_id', '=', sale.partner_id.id),
                ('state', 'in', ['sale', 'done']),
                ('id', '!=', sale.id),
            ],
            order='confirmation_date DESC',
            limit=1,
        )

        order_validated = (
            last_validated_order_order and
            (
                min_confirmation_date <=
                last_validated_order_order.confirmation_date <=
                max_confirmation_date
            ) and
            not
            last_validated_order_order.sale_order_which_use_me_in_program_id
        )
        return last_validated_order_order if order_validated else False

    @api.multi
    def _check_another_order_validated(self, sale):
        """ Check if the sale order customer has another sale order validated
        """
        return self.get_another_order_validated(sale)
