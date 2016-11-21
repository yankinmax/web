# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from datetime import date
from dateutil.relativedelta import relativedelta

from openerp.addons import decimal_precision as dp
from openerp.tools import float_compare

from openerp import api, fields, models, SUPERUSER_ID, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_sponsored = fields.Boolean(
        compute='_compute_is_sponsored'
    )

    generated_voucher_ids = fields.One2many(
        comodel_name='sale.discount.program',
        inverse_name='source_sale_id'
    )

    discount_manually_percent = fields.Float(
        string='Manually Discount (%)',
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    @api.depends(
        'pricelist_id',
        'partner_id', 'partner_id.sponsor_id', 'partner_id.sponsor_id.active'
    )
    def _compute_is_sponsored(self):
        sponsor_pricelist = self.env.ref('scenario.pricelist_sponsorship')
        for sale in self:
            if not sponsor_pricelist:
                sale.is_sponsored = False
            else:
                sale.is_sponsored = sale.partner_id.sponsor_id.active \
                    and sale.pricelist_id == sponsor_pricelist

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        """ Modify the domain of program_code_ids field in form view because
        the domain depens on connected user company.
        """
        result = super(SaleOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu
        )

        if view_type == 'form':
            eview = etree.fromstring(result['arch'])
            nodes = eview.xpath("//field[@name='program_code_ids']")
            if nodes:
                nodes[0].set(
                    'domain',
                    "['|', "

                    "'&', ('promo_code', '!=', False), "
                    "('code_valid', '=', True),"

                    "'&', '&', "
                    "('voucher_code', '!=', False), "
                    "('code_valid', '=', True), "
                    "('partner_company_id', '=', %d)"
                    "]"
                    % self.env.user.company_id.id
                )
            result['arch'] = etree.tostring(eview)

        return result

    @api.multi
    def create_partner_voucher(self, partner_id):
        self.ensure_one()
        months_validity = int(self.env['ir.config_parameter'].get_param(
            'voucher_default_validity', '0'
        ))

        expiration_date = None
        if months_validity:
            expiration_date = date.today() + relativedelta(
                months=months_validity
            )

        self.sudo().write({
            'generated_voucher_ids': [(0, False, {
                'partner_id': partner_id,
                'combinable': True,
                'voucher_code': self.env['ir.sequence'].next_by_code(
                    'discount.program.voucher_code'
                ),
                'voucher_amount': self.get_voucher_amount(),
                'max_use': 1,
                'expiration_date': expiration_date,
            })]
        })

    @api.multi
    def get_voucher_amount(self):
        """ Compute the amount for the voucher based on invoice amount.
        """
        self.ensure_one()
        icp = self.env['ir.config_parameter']
        percent = float(icp.get_param('voucher_percent', '10'))
        max_amount = int(icp.get_param('voucher_max_amount', '100'))

        amount = min(
            self.amount_total * percent / 100,
            max_amount
        )
        return amount

    @api.multi
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()

        for sale in self:
            # Bon d'achat si la commande a utilisé le programme de
            # parainnage et si le parrain est toujours valide
            if sale.is_sponsored:
                sale.create_partner_voucher(
                    sale.partner_id.sponsor_id.partner_id.id
                )

            # Bon d'achat pour chaque commande
            sale.create_partner_voucher(sale.partner_id.id)

    @api.multi
    def action_cancel(self):
        result = super(SaleOrder, self).action_cancel()

        # Delete unused vouchers
        for program in self.mapped('generated_voucher_ids'):
            if program.nb_use == 0:
                program.sudo().unlink()

        return result

    @api.one
    @api.constrains('discount_manually_percent')
    def _check_discount_manually_percent(self):
        settings_model = self.env['sale.config.settings']
        percent = settings_model.get_default_discount_manually_percent_max(
            None
        )['discount_manually_percent_max']
        if float_compare(
                self.discount_manually_percent,
                percent,
                self.env['decimal.precision'].precision_get('Discount')
        ) == 1:
            message = _(
                'Max manually discount allowed is %s %% for a sale order.'
            ) % percent
            raise exceptions.ValidationError(message)

    @api.onchange('discount_manually_percent')
    def _onchange_discount_manually_percent(self):
        self._check_discount_manually_percent()

    @api.multi
    def apply_discount_programs(self):
        self.ensure_one()
        super(SaleOrder, self).apply_discount_programs()
        if self.discount_manually_percent:
            for line in self.order_line:
                if not line.source_program_id:
                    line.discount += self.discount_manually_percent


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    can_edit_price_unit = fields.Boolean(
        compute='_compute_can_edit_price_unit'
    )
    price_unit_readonly = fields.Float(
        'Unit Price',
        related='price_unit',
        readonly=True,
    )

    @api.depends()
    def _compute_can_edit_price_unit(self):
        """ price_unit is editable only for admin and Depiltech Admin.
        """
        admin = self.env.user.id == SUPERUSER_ID or self.env.user.has_group(
            'specific_base.group_admin_depiltech'
        )
        for line in self:
            line.can_edit_price_unit = admin

    @api.onchange('price_unit_readonly')
    def onchange_price_unit_readonly(self):
        self.price_unit = self.price_unit_readonly
