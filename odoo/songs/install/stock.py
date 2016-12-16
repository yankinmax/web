# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from anthem.lyrics.records import create_or_update

import anthem


@anthem.log
def create_stock_warehouse(ctx):
    ir_model_data = ctx.env['ir.model.data']
    companies = ctx.env['res.company'].search([
        ('name', '!=', 'Depil Tech Holding'),
    ])
    for company in companies:
        model_data = ir_model_data.search([
            ('model', '=', 'res.company'),
            ('res_id', '=', company.id)
        ])
        if model_data:
            data_name = model_data.name.replace('company_', '')
            create_or_update(
                ctx,
                'stock.warehouse',
                'scenario.warehouse_%s' % data_name,
                {
                    'code': 'wh_%s' % data_name,
                    'name': 'Stock %s' % company.name,
                    'company_id': company.id,
                }
            )


@anthem.log
def main(ctx):
    create_stock_warehouse(ctx)
