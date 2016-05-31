# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @intercompany_rules
  Scenario Outline: configure invoice intercompany rules
  Given I find a "res.company" with oid: <company>
    And having:
     | name                         | value             |
     | auto_generate_invoices       | True              |
     | intercompany_user_id         | by oid: <user>    |
     Examples: companies
      | company             | user           |
      | base.main_company   | base.user_root |
      | scen.agency_succ_mx | scen.user_mx   |
      | scen.agency_succ_CH | scen.user_CH   |
      | scen.agency_succ_be | scen.user_be   |
      | scen.agency_succ_lu | scen.user_lu   |
      | scen.agency_holding | scen.user_ah   |
      | scen.agency_center1 | scen.user_c1   |
      | scen.agency_center2 | scen.user_c2   |
      | scen.agency_center3 | scen.user_c3   |
      | scen.agency_center4 | scen.user_c4   |
      | scen.agency_center5 | scen.user_c5   |
