# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @admin_dt_group
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
      | Extra Rights / Multi Companies     |
      | Admin DT                           |
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