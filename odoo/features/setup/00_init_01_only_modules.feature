# -*- coding: utf-8 -*-
@depiltech @setup_only_modules

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @modules
  Scenario: install modules
    Given I install the required modules with dependencies
      | name                                 |
      # oca/ocb
      | account_cancel                       |
      | sale                                 |
      | crm                                  |
      | survey                               |
      | l10n_be                              |
      | l10n_ch                              |
      | l10n_fr                              |
      | l10n_lu                              |
      | l10n_mx                              |
      # OCA addons
      | web_easy_switch_company              |
      | server_environment                   |
      | mail_environment                     |
      | l10n_fr_siret                        |
      | partner_firstname                    |
      | web_duplicate_visibility             |
      | partner_survey                       |
      | base_phone                           |
      | account_fiscal_year                  |
      | account_move_locking                 |
      | account_financial_report_qweb        |
      | account_bank_statement_import_ofx    |
      | account_banking_sepa_credit_transfer |
      # local-src
      | server_environment_files             |
      | report_page_endnote                  |
      | fields_regex_validation              |
      | specific_base                        |
      | specific_discount_program            |
      | specific_payment_mode                |
