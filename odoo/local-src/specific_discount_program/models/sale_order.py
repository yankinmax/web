# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _prepare_invoice(self):
        """ Specified on invoice if sponsorship program was used in sale.order
        """
        self.ensure_one()
        vals = super(SaleOrder, self)._prepare_invoice()

        vals['sale_partner_id'] = self.partner_id.id

        if self.pricelist_id == self.env.ref('scenario.pricelist_sponsorship'):
            vals['sponsor_id'] = self.partner_id.sponsor_id.id

        return vals
