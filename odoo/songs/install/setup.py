# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream
from anthem.lyrics.records import create_or_update
from ..common import req
from ..common import define_settings


@anthem.log
def discount_config(ctx):
    """ discount_config
     (05_sale_discount.feature) """
    values = {
        'key': 'force_discount_apply',
        'value': True,
    }
    create_or_update(ctx, 'ir.config_parameter',
                     'force_discount_apply',
                     values)

    values = {
        'key': 'voucher_default_validity',
        'value': 10,
    }
    create_or_update(ctx, 'ir.config_parameter',
                     'voucher_default_validity',
                     values)

    values = {
        'key': 'voucher_max_count',
        'value': 2,
    }
    create_or_update(ctx, 'ir.config_parameter',
                     'voucher_max_count',
                     values)

    values = {
        'key': 'voucher_max_amount',
        'value': 100,
    }
    create_or_update(ctx, 'ir.config_parameter',
                     'voucher_max_amount',
                     values)

    values = {
        'key': 'voucher_percent',
        'value': 10,
    }
    create_or_update(ctx, 'ir.config_parameter',
                     'voucher_percent',
                     values)


@anthem.log
def multicompany_base_finance_accounting_settings(ctx):
    """ multicompany_base_finance_accounting_settings
     (01_accounting.feature) """
    define_settings(
        ctx,
        'base.config.settings',
        {
            'group_light_multi_company': True,
            'module_inter_company_rules': True,
            'company_share_partner': False,
        })


@anthem.log
def sale_pricelist(ctx):
    """ sale_pricelist
     (01_accounting.feature) """
    define_settings(
        ctx,
        'sale.config.settings',
        {
            'sale_pricelist_setting': 'formula',
            'group_sale_pricelist': True,
            'group_pricelist_item': True,
        })


@anthem.log
def admin_user(ctx):
    """ admin_user
     (02_users.feature) """
    ctx.env.user.company_ids = ctx.env.ref('base.main_company').ids
    groups = [
        ctx.env.ref('account.group_account_manager'),
        ctx.env.ref('purchase.group_purchase_manager'),
        ctx.env.ref('sales_team.group_sale_manager'),
        ctx.env.ref('sales_team.group_sale_salesman'),
        ctx.env.ref('sales_team.group_sale_salesman_all_leads'),
        ctx.env.ref('base.group_no_one'),
        ctx.env.ref('base.group_multi_currency'),
        ctx.env.ref('base.group_multi_company'),
    ]
    group_ids = [g.id for g in groups]
    curr_groups = [g.id for g in ctx.env.user.groups_id]
    ctx.env.user.group_id = list(set(group_ids + curr_groups))


@anthem.log
def intercompany_invoice(ctx):
    """ intercompany_invoice
     (02_users.feature) """
    ctx.env.ref('base.main_partner').company_id = False


@anthem.log
def order_line_discount(ctx):
    """ order_line_discount
     (05_sale_discount.feature) """
    define_settings(
        ctx,
        'sale.config.settings',
        {
            'group_discount_per_so_line': 1,
        })


@anthem.log
def discount_pricelist(ctx):
    """ discount_pricelist
     (05_sale_discount.feature) """
    values = {
        'name': 'Parrainage',
        'discount_policy': 'without_discount',
        'item_ids': False,
    }
    create_or_update(ctx, 'product.pricelist',
                     'scenario.pricelist_sponsorship',
                     values)

    values = {
        'pricelist_id': ctx.env.ref('scenario.pricelist_sponsorship').id,
        'applied_on': '3_global',
        'compute_price': 'percentage',
        'percent_price': 10,
    }
    create_or_update(ctx, 'product.pricelist.item',
                     'scenario.pricelist_sponsorship_item1',
                     values)

    values = {
        'name': 'Code promo',
        'discount_policy': 'without_discount',
        'item_ids': False,
    }
    create_or_update(ctx, 'product.pricelist',
                     'scenario.pricelist_code_promo',
                     values)

    values = {
        'pricelist_id': ctx.env.ref('scenario.pricelist_code_promo').id,
        'applied_on': '3_global',
        'compute_price': 'percentage',
        'percent_price': 10,
    }
    create_or_update(ctx, 'product.pricelist.item',
                     'scenario.pricelist_code_promo_item1',
                     values)


@anthem.log
def survey_survey_import(ctx):
    """ survey_survey_import
     (06_imports.feature) """
    content = resource_stream(req, 'data/setup/survey.survey.csv')
    load_csv_stream(ctx, 'survey.survey', content, delimiter=',')


@anthem.log
def survey_page_import(ctx):
    """ survey_page_import
     (06_imports.feature) """
    content = resource_stream(req, 'data/setup/survey.page.csv')
    load_csv_stream(ctx, 'survey.page', content, delimiter=',')


@anthem.log
def survey_question_import(ctx):
    """ survey_question_import
     (06_imports.feature) """
    content = resource_stream(req, 'data/setup/survey.question.csv')
    load_csv_stream(ctx, 'survey.question', content, delimiter=',')


@anthem.log
def product_category_import(ctx):
    """ product_category_import
     (06_imports.feature) """
    content = resource_stream(req, 'data/setup/product.category.csv')
    load_csv_stream(ctx, 'product.category', content, delimiter=';')


@anthem.log
def product_product_import(ctx):
    """ product_product_import
     (06_imports.feature) """
    content = resource_stream(req, 'data/install/10.product - all.csv')
    load_csv_stream(ctx, 'product.product', content, delimiter=',')

    content = resource_stream(req, 'data/install/11.product - new.csv')
    load_csv_stream(ctx, 'product.product', content, delimiter=',')


@anthem.log
def sale_discount_program_import(ctx):
    """ sale_discount_program_import
     (06_imports.feature) """
    content = resource_stream(req, 'data/setup/sale.discount.program.csv')
    load_csv_stream(ctx, 'sale.discount.program', content, delimiter=',')


@anthem.log
def main(ctx):
    discount_config(ctx)
    multicompany_base_finance_accounting_settings(ctx)
    sale_pricelist(ctx)
    admin_user(ctx)
    intercompany_invoice(ctx)
    order_line_discount(ctx)
    discount_pricelist(ctx)
    survey_survey_import(ctx)
    survey_page_import(ctx)
    survey_question_import(ctx)
    product_category_import(ctx)
    product_product_import(ctx)
    sale_discount_program_import(ctx)
