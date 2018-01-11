# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PartnerSponsor(models.Model):
    _name = 'partner.sponsor'

    partner_id = fields.Many2one(
        'res.partner',
        required=True, ondelete='cascade',
        string='Partner'
    )

    name = fields.Char(compute='_compute_name', store=True)

    active = fields.Boolean(
        compute='_compute_active',
        store=True,
    )

    @api.depends('partner_id.name', 'partner_id.city')
    def _compute_name(self):
        for sponsor in self:
            name = sponsor.partner_id.name
            if sponsor.partner_id.city:
                name = "%s - %s" % (name, sponsor.partner_id.city)

            sponsor.name = name

    @api.depends('partner_id.active', 'partner_id.already_bought')
    def _compute_active(self):
        for sponsor in self:
            sponsor.active = sponsor.partner_id.already_bought
