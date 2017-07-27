# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem

from . import base_vars
from ..common import load_csv
from anthem.lyrics.records import create_or_update


@anthem.log
def base_conf(ctx):
    """ Configuring analytic for purchase/sale """
    account_settings = ctx.env['account.config.settings']
    for company_xml_id, coa in base_vars.coa_dict.iteritems():
        company = ctx.env.ref(company_xml_id)
        acs = account_settings.with_context(company_id=company.id).create(
            {'group_analytic_accounting': True,
             'group_multi_currency': True,
             'group_analytic_account_for_purchases': True,
             'tax_calculation_rounding_method': 'swedish_round_globally',
             }
        )
        acs.execute()


@anthem.log
def update_code_digits(ctx):
    for company_xml_id, coa in base_vars.coa_dict.iteritems():
        ctx.env['account.config.settings'].create(
            {'company_id': ctx.env.ref(company_xml_id).id,
             'code_digits': 4}
        ).execute()


@anthem.log
def create_account_payment_mode(ctx):
    """ import new account_journal """
    sepa = ctx.env.ref(
        'account_banking_sepa_credit_transfer.sepa_credit_transfer')
    # MTS account.payment.mode
    jour_bank_mts = ctx.env['account.journal'].search([
        ('name', '=', 'Bank'),
        ('type', '=', 'bank'),
        ('company_id', '=', ctx.env.ref('base.main_company').id)])
    jour_vendor_mts = ctx.env['account.journal'].search([
        ('name', '=', 'Vendor Bills'),
        ('type', '=', 'purchase'),
        ('company_id', '=', ctx.env.ref('base.main_company').id)])
    values = {
        'name': 'Paiements SEPA',
        'company_id': ctx.env.ref('base.main_company').id,
        'active': True,
        'payment_method_id': sepa.id,
        'bank_account_link': 'fixed',
        'fixed_journal_id': jour_bank_mts.id,
        'default_journal_ids': [(6, 0, jour_vendor_mts.ids)],
        'default_payment_mode': 'any',
        'default_target_move': 'posted',
    }
    create_or_update(ctx, 'account.payment.mode',
                     '__setup__.account_payment_mode_mts_sepa', values)

    # MTE account.payment.mode
    jour_bank_mte = ctx.env['account.journal'].search([
        ('name', '=', 'Bank'),
        ('type', '=', 'bank'),
        ('company_id', '=', ctx.env.ref('__setup__.company_mte').id)])
    jour_vendor_mte = ctx.env['account.journal'].search([
        ('name', '=', 'Vendor Bills'),
        ('type', '=', 'purchase'),
        ('company_id', '=', ctx.env.ref('__setup__.company_mte').id)])
    values = {
        'name': 'Paiements SEPA',
        'company_id': ctx.env.ref('__setup__.company_mte').id,
        'active': True,
        'payment_method_id': sepa.id,
        'bank_account_link': 'fixed',
        'fixed_journal_id': jour_bank_mte.id,
        'default_journal_ids': [(6, 0, jour_vendor_mte.ids)],
        'default_payment_mode': 'any',
        'default_target_move': 'posted',
    }
    create_or_update(ctx, 'account.payment.mode',
                     '__setup__.account_payment_mode_mte_sepa', values)


@anthem.log
def journal_cancel(ctx):
    """ Allow canceling entries on journal """
    journals = ctx.env['account.journal'].search([])
    for journal in journals:
        journal.write({'update_posted': True})


@anthem.log
def load_journals(ctx):
    model = ctx.env['account.journal'].with_context({'tracking_disable': 1})
    load_csv(ctx, 'data/install/account.journal.csv', model)


@anthem.log
def set_pain_method(ctx):
    sepa = ctx.env.ref(
        'account_banking_sepa_credit_transfer.sepa_credit_transfer')
    sepa.write({'pain_version': 'pain.001.001.03.ch.02'})


@anthem.log
def main(ctx):
    """ Configuring accounting """
    base_conf(ctx)
    update_code_digits(ctx)
    create_account_payment_mode(ctx)
    journal_cancel(ctx)
    load_journals(ctx)
    set_pain_method(ctx)
