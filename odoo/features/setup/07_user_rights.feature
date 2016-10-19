# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @company_admin_users_groups
  Scenario Outline: Add correct groups to administrators
    Given I find a "res.users" with oid: <user_oid>
    And we assign to user the groups below
      | group_name                                  |
      | Accounting & Finance / Adviser              |
      | Purchases / Manager                         |
      | Sales / Manager                             |
      | Extra Rights / Technical Features           |
      | Inventory / Manager                         |
      | Lead Automation / Manager                   |
      | Administration / Settings                   |
      | Extra Rights / Multi Companies              |
      | Technical Settings / Sales Pricelists       |
      | Technical Settings / Manage Pricelist Items |
      | Admin DT                                    |

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
      | scen.user_adm_mx_1 |
      | scen.user_adm_be_1 |
      | scen.user_adm_fr_1 |
      | scen.user_adm_ch_1 |
      | scen.user_adm_lu_1 |

  @company_normal_users_groups
  Scenario Outline: Add correct groups to administrators
    Given I find a "res.users" with oid: <user_oid>
    And we assign to user the groups below
      | group_name                                  |
      | Accounting & Finance / Accountant           |
      | Purchases / User                            |
      | Sales / See all Leads                       |
      | Extra Rights / Technical Features           |
      | Inventory / User                            |
      | Lead Automation / User                      |
      | Technical Settings / Sales Pricelists       |
      | Technical Settings / Manage Pricelist Items |
    Examples: users
      | user_oid       |
      | scen.user_mx   |
      | scen.user_CH   |
      | scen.user_be   |
      | scen.user_lu   |
      | scen.user_ah   |
      | scen.user_c1   |
      | scen.user_c2   |
      | scen.user_c3   |
      | scen.user_c4   |
      | scen.user_c5   |
      | scen.user_mx_1 |
      | scen.user_be_1 |
      | scen.user_fr_1 |
      | scen.user_ch_1 |
      | scen.user_lu_1 |
