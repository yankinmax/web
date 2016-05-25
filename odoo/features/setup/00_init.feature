# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @no_login
  Scenario: CREATE DATABASE
    Given I find or create database from config file

  @company
  Scenario: SETUP company informations
    Given I need a "res.company" with oid: base.main_company
    And having
       | key        | value              |
       | name       | Depil'Tech Holding |
       | country_id | by oid: base.fr    |
    # Given the company has the "images/logo.png" logo

  @no_demo_data
  Scenario: deactivate demo data
    Given I update the module list
    And I do not want all demo data to be loaded on install

  @lang
  Scenario: install lang
   Given I install the following language :
      | lang  |
      | fr_FR |
      | es_MX |
    Then the language should be available
   Given I find a "res.lang" with code: fr_FR
    And having:
      | key           | value    |
      | grouping      | [3,0]    |
      | date_format   | %d/%m/%Y |
      | thousands_sep | .        |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_holding
    And having:
       | key          | value                     |
       | name         | Agencies Holding          |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_holding
    And having:
       | key         | value                               |
       | name        | Agencies Holding                    |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: FR                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_agency_holding |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_center1
    And having:
       | key          | value                     |
       | name         | Agency/Center 1           |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_center1
    And having:
       | key         | value                               |
       | name        | Agency/Center 1                     |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: FR                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_agency_center1 |
       | parent_id   | by oid: scen.agency_holding         |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_center2
    And having:
       | key          | value                     |
       | name         | Agency/Center 2           |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_center2
    And having:
       | key         | value                               |
       | name        | Agency/Center 2                     |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: FR                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_agency_center2 |
       | parent_id   | by oid: scen.agency_holding         |


  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_center3
    And having:
       | key          | value                     |
       | name         | Agency/Center 3           |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_center3
    And having:
       | key         | value                               |
       | name        | Agency/Center 3                     |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: FR                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_agency_center3 |
       | parent_id   | by oid: scen.agency_holding         |


  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_center4
    And having:
       | key          | value                     |
       | name         | Agency/Center 4           |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_center4
    And having:
       | key         | value                               |
       | name        | Agency/Center 4                     |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: FR                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_agency_center4 |
       | parent_id   | by oid: scen.agency_holding         |


  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_center5
    And having:
       | key          | value                     |
       | name         | Agency/Center 5           |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_center5
    And having:
       | key         | value                               |
       | name        | Agency/Center 5                     |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: FR                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_agency_center5 |
       | parent_id   | by oid: scen.agency_holding         |


  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_succ_be
    And having:
       | key          | value                     |
       | name         | Agency BE                 |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: BE               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_succ_be
    And having:
       | key         | value                               |
       | name        | Agency BE                           |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: BE                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_succ_be        |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_succ_lu
    And having:
       | key          | value                     |
       | name         | Agency LU                 |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: LU               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_succ_lu
    And having:
       | key         | value                               |
       | name        | Agency LU                           |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: LU                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | currency_id | by name: EUR                        |
       | partner_id  | by oid: scen.partner_succ_lu        |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_succ_ch
    And having:
       | key          | value                     |
       | name         | Agency CH                 |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: CH               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_succ_CH
    And having:
       | key         | value                               |
       | name        | Agency CH                           |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: CH                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | partner_id  | by oid: scen.partner_succ_ch        |
  Given I set the context to "{"active_test": False}"
    And I find a "res.company" with oid: scen.agency_succ_CH
    And having:
       | key         | value                               |
       | currency_id | by oid: base.CHF                    |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_succ_mx
    And having:
       | key          | value                     |
       | name         | Agency MX                 |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: MX               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_succ_mx
    And having:
       | key         | value                               |
       | name        | Agency MX                           |
       | street      |                                     |
       | street2     |                                     |
       | zip         |                                     |
       | city        |                                     |
       | country_id  | by code: MX                         |
       | phone       | +33 00 000 00 00                    |
       | fax         | +33 00 000 00 00                    |
       | website     |                                     |
       | partner_id  | by oid: scen.partner_succ_mx        |

  @modules
  Scenario: install modules
    Given I install the required modules with dependencies
        | name                    |
        # oca/ocb
        | account                 |
        | sale                    |
        | crm                     |
        # | l10n_fr                 |
        # | l10n_mx                 |
        # | l10n_ch                 |
        # | l10n_lu                 |
        # | survey                  |
        | web_easy_switch_company |
        # OCA/server-tools
        # | disable_openerp_online  |
        # local-src
   Given I set the context to "{"active_test": False}"
    And I find a "res.company" with oid: scen.agency_succ_mx
    And having:
       | key         | value                               |
       | currency_id | by oid: base.MXN                    |

   Scenario: configure users
    Given I find a "res.users" with login: admin
     And having:
      | key         | value                               |
      | company_ids | by oid: base.main_company           |
      | company_ids | add all by oid: scen.agency_succ_mx |
      | company_ids | add all by oid: scen.agency_succ_CH |
      | company_ids | add all by oid: scen.agency_succ_be |
      | company_ids | add all by oid: scen.agency_succ_lu |
      | company_ids | add all by oid: scen.agency_holding |
      | company_ids | add all by oid: scen.agency_center1 |
      | company_ids | add all by oid: scen.agency_center2 |
      | company_ids | add all by oid: scen.agency_center3 |
      | company_ids | add all by oid: scen.agency_center4 |
      | company_ids | add all by oid: scen.agency_center5 |
    And we assign to user the groups below
      | group_name                         |
      | Accounting & Finance / Adviser     |
      | Purchases / Manager                |
      | Sales / Manager                    |
      | Sales / See Own Leads              |
      | Sales / See all Leads              |
      | Extra Rights / Technical Features  |
      | Extra Rights / Multi Currencies    |
      | Extra Rights / Multi Companies     |


  @multicompany_base_finance_accounting_settings
  Scenario: BASE SETTINGS multi-company multi-currency + do not share partners between companies
  Given I need a "base.config.settings" with oid: scen.base_settings_main_cpy
     And having:
     | name                              | value                        |
     | group_light_multi_company         | True                         |
     | module_inter_company_rules        | True                         |
     | company_share_partner             | False                        |
   Then execute the setup

  @acc_cfg_mx
  Scenario: config accounting for Mexico
  Given I am configuring the company with ref "scen.agency_succ_mx"
  And I install the required modules with dependencies
        | name                    |
        | l10n_mx                 |

  @acc_cfg_mx2
  Scenario: config accounting for Mexico
  Given I need a "account.config.settings" with oid: scen.acc_cfg_mx
    And having:
     | name                         | value                                    |
     | company_id                   | by oid: scen.agency_succ_mx              |
     | chart_template_id            | by oid: l10n_mx.vauxoo_mx_chart_template |
     | template_transfer_account_id | by oid: l10n_mx.cuenta1129003000         |
     | sale_tax_id          | by oid: l10n_mx.tax12                            |
     | purchase_tax_id      | by oid: l10n_mx.tax14                            |
     Then execute the setup

  @acc_cfg_ch
  Scenario: config accounting for Mexico
  Given I am configuring the company with ref "scen.agency_succ_CH"
  And I install the required modules with dependencies
        | name                    |
        | l10n_ch                 |

  @acc_cfg_ch2
  Scenario: config accounting for Switzerland
  Given I need a "account.config.settings" with oid: scen.acc_cfg_ch
    And having:
     | name                         | value                                    |
     | company_id                   | by oid: scen.agency_succ_CH              |
     | chart_template_id            | by oid: l10n_ch.l10nch_chart_template    |
     | template_transfer_account_id | by oid: l10n_ch.transfer_account_id      |
     | sale_tax_id                  | by oid: l10n_ch.vat_80_incl              |
     | purchase_tax_id              | by oid: l10n_ch.vat_80_purchase_incl     |
     Then execute the setup