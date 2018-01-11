# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sponsor_id = fields.Many2one('partner.sponsor', 'Sponsor')

    already_bought = fields.Boolean(
        compute='_compute_already_bought',
        store=True
    )

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        if partner.company_type == 'agency_customer':
            self.env['partner.sponsor'].create({'partner_id': partner.id})

        return partner

    @api.multi
    def unlink(self):
        self.env['partner.sponsor'].with_context(active_test=False).search(
            [('partner_id', 'in', self.ids)]).unlink()
        super(ResPartner, self).unlink()

    @api.depends('sale_order_ids', 'sale_order_ids.state')
    def _compute_already_bought(self):
        """ True if partner has a confirmed or done sale.order
        """
        for partner in self:
            partner.already_bought = bool(
                partner.sale_order_ids.filtered(
                    lambda s: s.state in ('sale', 'done')
                )
            )
