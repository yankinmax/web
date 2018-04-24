# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import anthem
from anthem.lyrics.records import add_xmlid


@anthem.log
def change_engagements_bi_sql_view_xmlid(ctx):
    """ Changing the XMLID of BI SQL View engagements """
    old_xmlid = '__export__.bi_sql_view_1'
    bi_view_engagements = ctx.env.ref(old_xmlid, raise_if_not_found=False)
    if bi_view_engagements:
        module, name = old_xmlid.split('.')
        ir_model_data = ctx.env['ir.model.data'].search(
            [('module', '=', module), ('name', '=', name)])
        if ir_model_data:
            ir_model_data.unlink()
    else:
        bi_view_engagements = ctx.env['bi.sql.view'].search([
            ('technical_name', '=', 'engagements')
        ])
    if bi_view_engagements:
        add_xmlid(ctx, bi_view_engagements,
                  '__setup__.bi_sql_view_engagements', noupdate=True)


@anthem.log
def main(ctx):
    """ Applying update 10.9.0 """
    change_engagements_bi_sql_view_xmlid(ctx)
