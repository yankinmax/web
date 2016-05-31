# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

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

  @currency_mx
  Scenario: currency_mx
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
  Scenario: config accounting for Switzerland
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

  @acc_cfg_lu
  Scenario: config accounting for Luxembourg
  Given I am configuring the company with ref "scen.agency_succ_lu"
  And I install the required modules with dependencies
        | name                    |
        | l10n_lu                 |

  @acc_cfg_lu2
  Scenario: config accounting for Luxembourg
  Given I need a "account.config.settings" with oid: scen.acc_cfg_lu
    And having:
     | name                         | value                                    |
     | company_id                   | by oid: scen.agency_succ_lu              |
     | chart_template_id            | by oid: l10n_lu.lu_2011_chart_1          |
     | template_transfer_account_id | by oid: l10n_lu.lu_2011_account_517      |
     | sale_tax_id                  | by oid: l10n_lu.lu_2015_tax_V-ART-43_60b |
     | purchase_tax_id              | by oid: l10n_lu.lu_2011_tax_AB-EC-0      |
     Then execute the setup

  @acc_cfg_be
  Scenario: config accounting for Belgium
  Given I am configuring the company with ref "scen.agency_succ_be"
  And I install the required modules with dependencies
        | name                    |
        | l10n_be                 |

  @acc_cfg_be2
  Scenario: config accounting for Belgium
  Given I need a "account.config.settings" with oid: scen.acc_cfg_be
    And having:
     | name                         | value                                    |
     | company_id                   | by oid: scen.agency_succ_be              |
     | chart_template_id            | by oid: l10n_be.l10nbe_chart_template    |
     | template_transfer_account_id | by oid: l10n_be.trans                    |
     | sale_tax_id                  | by oid: l10n_be.attn_VAT-OUT-21-S        |
     | purchase_tax_id              | by oid: l10n_be.attn_VAT-IN-V81-21       |
     Then execute the setup

  @acc_centers
  Scenario Outline: configure l10n_fr for all centers
  Given I need a "account.config.settings" with oid: <c_oid>
    And having:
     | name                         | value                                      |
     | company_id                   | by oid: <company>                          |
     | chart_template_id            | by oid: l10n_fr.l10n_fr_pcg_chart_template |
     | template_transfer_account_id | by oid: l10n_fr.pcg_58                     |
     | sale_tax_id                  | by oid: l10n_fr.tva_normale                |
     | purchase_tax_id              | by oid: l10n_fr.tva_acq_normale            |
     Then execute the setup
     Examples: companies
      | c_oid               | company             |
      | scen.acc_cfg_ah     | scen.agency_holding |
      | scen.acc_cfg_c1     | scen.agency_center1 |
      | scen.acc_cfg_c2     | scen.agency_center2 |
      | scen.acc_cfg_c3     | scen.agency_center3 |
      | scen.acc_cfg_c4     | scen.agency_center4 |
      | scen.acc_cfg_c5     | scen.agency_center5 |