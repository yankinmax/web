# -*- coding: utf-8 -*-
@depiltech @center_template

Feature: Template for a center to be deployed easily

  @company_template
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scen.partner_agency_center_XXX
    And having:
       | key          | value                     |
       | name         | Agency/Center_XXX         |
       | street       |                           |
       | street2      |                           |
       | zip          |                           |
       | city         |                           |
       | country_id   | by code: FR               |
       | phone        | +33 00 000 00 00          |
       | fax          | +33 00 000 00 00          |
       | website      |                           |
       | company_type | company                   |
  Given I need a "res.company" with oid: scen.agency_center_XXX
    And having:
       | key         | value                                  |
       | name        | Agency/Center_XXX                      |
       | street      |                                        |
       | street2     |                                        |
       | zip         |                                        |
       | city        |                                        |
       | country_id  | by code: FR                            |
       | phone       | +33 00 000 00 00                       |
       | fax         | +33 00 000 00 00                       |
       | website     |                                        |
       | currency_id | by name: EUR                           |
       | partner_id  | by oid: scen.partner_agency_center_XXX |
       | parent_id   | by oid: scen.agency_holding            |

  @intercompany_invoice_template
  Scenario Outline: remove company_id from partners linked to a company
    Given I find a "res.partner" with oid: <p_oid>
    And having:
      | key                    | value |
      | company_id             | False |
    Examples: Partner ids
      | p_oid                          |
      | scen.partner_agency_center_XXX |

  @users_template
  Scenario: Configure main partner and company
  Given I find a "res.users" with oid: base.user_root
     And having:
      | key         | value                                |
      | company_ids | add all by oid: scen.agency_succ_XXX |
  Given I find a "res.users" with oid: scen.user_admin_ah
     And having:
      | key         | value                                |
      | company_ids | add all by oid: scen.agency_succ_XXX |

  @accounting_template
  Scenario: Configure accounting
  Given I need a "account.config.settings" with oid: scen.acc_cfg_ah
    And having:
     | name                         | value                                      |
     | company_id                   | by oid: scen.agency_center_XXX             |
     | chart_template_id            | by oid: l10n_fr.l10n_fr_pcg_chart_template |
     | template_transfer_account_id | by oid: l10n_fr.pcg_58                     |
     | sale_tax_id                  | by oid: l10n_fr.tva_normale                |
     | purchase_tax_id              | by oid: l10n_fr.tva_acq_normale            |
     Then execute the setup

  @company_users_template
  Scenario Outline: create and configure users
    Given I need a "res.users" with oid: <user_oid>
    And having:
      | key                    | value                 |
      | company_id             | by oid: <company_oid> |
      | company_ids            | by oid: <company_oid> |
      | name                   | <u_name>              |
      | login                  | <u_login>             |
      | password               | <password>            |
      | email                  | <email>               |
      | lang                   | <lang>                |
    Examples: users
      | user_oid            | company_oid            | u_name            | u_login   | password  | email                 | lang  |
      | scen.user_admin_XXX | scen.agency_center_XXX | Administrator XXX | admin_xxx | admin_XXX | admin_XXX@example.com | fr_FR |
      | scen.user_XXX       | scen.agency_center_XXX | User XXX          | user_xxx  | user_XXX  | user_XXX@example.com  | fr_FR |

  @company_admin_users_groups_template
  Scenario Outline: Add correct groups to administrators
    Given I find a "res.users" with oid: <user_oid>
    And we assign to user the groups below
      | group_name                         |
      | Accounting & Finance / Adviser     |
      | Purchases / Manager                |
      | Sales / Manager                    |
      | Sales / See Own Leads              |
      | Sales / See all Leads              |
      | Extra Rights / Technical Features  |
      | Inventory / Manager                |
      | Lead Automation / Manager          |
    Examples: users
      | user_oid            |
      | scen.user_admin_XXX |

  @company_normal_users_groups_template
  Scenario Outline: Add correct groups to user
    Given I find a "res.users" with oid: <user_oid>
    And we assign to user the groups below
      | group_name                         |
      | Accounting & Finance / Accountant  |
      | Purchases / User                   |
      | Sales / See all Leads              |
      | Extra Rights / Technical Features  |
      | Inventory / User                   |
      | Lead Automation / User             |
    Examples: users
      | user_oid      |
      | scen.user_XXX |

  @teleop_template_user_template
  Scenario: configure users
    Given I execute the SQL commands:
    """
    INSERT INTO res_company_users_rel (cid, user_id) VALUES (
      (SELECT res_id FROM ir_model_data WHERE module='scen' AND name='agency_center_XXX' AND model='res.company'),
      (SELECT res_id FROM ir_model_data WHERE module='scen' AND name='template_teleop_user' AND model='res.users')
    );
    """

  @intercompany_rules_template
  Scenario: configure invoice intercompany rules
  Given I find a "res.company" with oid: scen.agency_center_XXX
    And having:
     | name                         | value                 |
     | auto_generate_invoices       | True                  |
     | intercompany_user_id         | by oid: scen.user_XXX |
