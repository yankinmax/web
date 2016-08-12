# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @admin_user
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

  @intercompany_invoice
  Scenario Outline: remove company_id from partners linked to a company
    Given I find a "res.partner" with oid: <p_oid>
    And having:
      | key                    | value |
      | company_id             | False |
    Examples: Partner ids
      | p_oid                       |
      | base.main_partner           |
      | scen.partner_succ_mx        |
      | scen.partner_succ_ch        |
      | scen.partner_succ_be        |
      | scen.partner_succ_lu        |
      | scen.partner_agency_holding |
      | scen.partner_agency_center1 |
      | scen.partner_agency_center2 |
      | scen.partner_agency_center3 |
      | scen.partner_agency_center4 |
      | scen.partner_agency_center5 |

  @company_users
  Scenario Outline: create and configure users
    Given I set the context to "{"tracking_disable": True}"
    And I need a "res.users" with oid: <user_oid>
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
      | user_oid           | company_oid         | u_name           | u_login  | password | email                | lang  |
      | scen.user_admin_mx | scen.agency_succ_mx | Administrator mx | admin_mx | admin_mx | admin_mx@example.com | es_MX |
      | scen.user_admin_CH | scen.agency_succ_CH | Administrator CH | admin_CH | admin_CH | admin_CH@example.com | fr_FR |
      | scen.user_admin_be | scen.agency_succ_be | Administrator be | admin_be | admin_be | admin_be@example.com | fr_FR |
      | scen.user_admin_lu | scen.agency_succ_lu | Administrator lu | admin_lu | admin_lu | admin_lu@example.com | fr_FR |
      | scen.user_admin_ah | scen.agency_holding | Administrator ah | admin_ah | admin_ah | admin_ah@example.com | fr_FR |
      | scen.user_admin_c1 | scen.agency_center1 | Administrator c1 | admin_c1 | admin_c1 | admin_c1@example.com | fr_FR |
      | scen.user_admin_c2 | scen.agency_center2 | Administrator c2 | admin_c2 | admin_c2 | admin_c2@example.com | fr_FR |
      | scen.user_admin_c3 | scen.agency_center3 | Administrator c3 | admin_c3 | admin_c3 | admin_c3@example.com | fr_FR |
      | scen.user_admin_c4 | scen.agency_center4 | Administrator c4 | admin_c4 | admin_c4 | admin_c4@example.com | fr_FR |
      | scen.user_admin_c5 | scen.agency_center5 | Administrator c5 | admin_c5 | admin_c5 | admin_c5@example.com | fr_FR |
      | scen.user_mx       | scen.agency_succ_mx | User mx          | user_mx  | user_mx  | user_mx@example.com  | es_MX |
      | scen.user_CH       | scen.agency_succ_CH | User CH          | user_CH  | user_CH  | user_CH@example.com  | fr_FR |
      | scen.user_be       | scen.agency_succ_be | User be          | user_be  | user_be  | user_be@example.com  | fr_FR |
      | scen.user_lu       | scen.agency_succ_lu | User lu          | user_lu  | user_lu  | user_lu@example.com  | fr_FR |
      | scen.user_ah       | scen.agency_holding | User ah          | user_ah  | user_ah  | user_ah@example.com  | fr_FR |
      | scen.user_c1       | scen.agency_center1 | User c1          | user_c1  | user_c1  | user_c1@example.com  | fr_FR |
      | scen.user_c2       | scen.agency_center2 | User c2          | user_c2  | user_c2  | user_c2@example.com  | fr_FR |
      | scen.user_c3       | scen.agency_center3 | User c3          | user_c3  | user_c3  | user_c3@example.com  | fr_FR |
      | scen.user_c4       | scen.agency_center4 | User c4          | user_c4  | user_c4  | user_c4@example.com  | fr_FR |
      | scen.user_c5       | scen.agency_center5 | User c5          | user_c5  | user_c5  | user_c5@example.com  | fr_FR |

  @company_admin_users_groups
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
      | Administration / Settings          |
    Examples: users
      | user_oid           |
      | scen.user_admin_mx |
      | scen.user_admin_CH |
      | scen.user_admin_be |
      | scen.user_admin_lu |
      | scen.user_admin_ah |
      | scen.user_admin_c1 |
      | scen.user_admin_c2 |
      | scen.user_admin_c3 |
      | scen.user_admin_c4 |
      | scen.user_admin_c5 |

  @company_normal_users_groups
  Scenario Outline: Add correct groups to administrators
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
      | user_oid     |
      | scen.user_mx |
      | scen.user_CH |
      | scen.user_be |
      | scen.user_lu |
      | scen.user_ah |
      | scen.user_c1 |
      | scen.user_c2 |
      | scen.user_c3 |
      | scen.user_c4 |
      | scen.user_c5 |

  @teleop_template_user
  Scenario: configure users
    Given I set the context to "{"tracking_disable": True}"
    And I need a "res.users" with oid: scen.template_teleop_user
     And having:
      | key         | value                               |
      | name        | Teleop Template User                |
      | active      | False                               |
      | login       | teleop_tmpl                         |
      | email       | teleop_tmpl@example.com             |
      | lang        | fr_FR                               |
      | company_id  | by oid: scen.agency_holding         |
      | company_ids | by oid: scen.agency_holding         |
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
      | Inventory / Manager                |
      | Lead Automation / Manager          |
      | Administration / Settings          |
