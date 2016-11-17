# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class Program(models.Model):
    _inherit = 'sale.discount.program'

    allowed_company_ids = fields.Many2many(
        comodel_name='res.company',
        string='Allowed company',
    )

    partner_company_id = fields.Many2one(
        comodel_name='res.company',
        related='partner_id.company_id',
        store=True
    )

    # For vouchers created by sale.order
    source_sale_id = fields.Many2one(comodel_name='sale.order')

    _sql_constraints = [
        ('voucher_source_sale_id',
         'check(source_sale_id is null or voucher_code is not null)',
         _("source_sale_id can be filled only for voucher"))
    ]

    @api.depends(
        'program_name', 'voucher_code', 'promo_code', 'voucher_amount',
        'partner_id'
    )
    def _compute_name(self):
        for program in self:
            if program.voucher_code:
                program.name = "%s: %s (%s)" % (
                    program.partner_id.name,
                    program.voucher_code,
                    program.voucher_amount
                )

            else:
                super(Program, program)._compute_name()

    @api.model
    def create(self, vals):
        """ Set promo code not combinable
        """
        if vals.get('promo_code'):
            vals['combinable'] = False
        return super(Program, self).create(vals)

    @api.multi
    def check_voucher_limits(self, sale):
        super(Program, self).check_voucher_limits(sale)

        max_vouchers = int(self.env['ir.config_parameter'].get_param(
            'voucher_max_count', '0'
        ))
        if max_vouchers:
            nb_vouchers = len(sale.program_code_ids.filtered(
                lambda p: p.voucher_amount
            ))

            if nb_vouchers > max_vouchers:
                raise UserError(
                    _("Number of vouchers is limited to %s")
                    % max_vouchers
                )

    @api.model
    def get_automatic_program(self):
        domain = [
            '&',
            ('automatic', '=', True),
            '|',
            ('allowed_company_ids', '=', False),
            ('allowed_company_ids', 'parent_of', self.env.user.company_id)
        ]

        return self.search(domain)
