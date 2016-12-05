# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import anthem


@anthem.log
def product_taxes(ctx):
    sale_taxes = ctx.env['account.tax'].search([
        ('description', '=', '20.0'),
        ('type_tax_use', '=', 'sale'),
    ])

    purchase_taxes = ctx.env['account.tax'].search([
        ('description', '=', 'ACH-20.0'),
        ('type_tax_use', '=', 'purchase'),
    ])

    ctx.env['product.template'].search([]).write({
        'taxes_id': [(6, False, sale_taxes.mapped('id'))],
        'supplier_taxes_id': [(6, False, purchase_taxes.mapped('id'))],
    })

    # Produits sans TVA
    sale_taxes_0 = ctx.env['account.tax'].search([
        ('description', '=', 'EXPORT-0'),
        ('type_tax_use', '=', 'sale'),
    ])
    ctx.env.ref(
        'scenario.'
        'product_transfertdossier_fiche_client_sans_tva_product_template'
    ).write({
        'taxes_id': [(6, False, sale_taxes_0.mapped('id'))],
        'supplier_taxes_id': [(5,)],
    })

    ctx.env.ref(
        'sale_discount_program.product_voucher_product_template'
    ).write({
        'taxes_id': [(5,)],
        'supplier_taxes_id': [(5,)],
    })


@anthem.log
def create_tax_xmlid(ctx):
    ir_model_data = ctx.env['ir.model.data']
    taxes = ctx.env['account.tax'].search([])
    for tax in taxes:
        model_data = ir_model_data.search_count([
            ('model', '=', 'account.tax'),
            ('res_id', '=', tax.id)
        ])
        if not model_data:
            if tax.company_id:
                company_model_data = ir_model_data.search([
                    ('model', '=', 'res.company'),
                    ('res_id', '=', tax.company_id.id)
                ])
                company_xmlid_name = company_model_data.name
            else:
                company_xmlid_name = 'no_company'

            tax_name = tax.name.replace(' ', '_').replace('(', '_')
            tax_name = tax_name.replace(')', '_').replace('.', '_')
            tax_name = tax_name.replace('-', '_').replace(',', '_')

            ir_model_data.create({
                'name':
                    'account_tax_%s_%s_%s' % (
                        tax.type_tax_use,
                        company_xmlid_name,
                        tax_name,
                    ),
                'module': 'scenario',
                'model': 'account.tax',
                'res_id': tax.id
            })


@anthem.log
def main(ctx):
    product_taxes(ctx)
    create_tax_xmlid(ctx)
