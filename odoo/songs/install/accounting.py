# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import anthem


@anthem.log
def configure_taxes(ctx):
    """ Set sale tax TTC
    """
    ctx.env['account.tax'].search([
        ('description', '=', '20.0'),
        ('type_tax_use', '=', 'sale'),
    ]).write({
        'price_include': True
    })


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


@anthem.log
def main(ctx):
    configure_taxes(ctx)
    product_taxes(ctx)

