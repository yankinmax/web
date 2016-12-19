# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @multicompany_base_finance_accounting_settings
  Scenario: BASE SETTINGS multi-company multi-currency + do not share partners between companies
  Given I need a "base.config.settings" with oid: scen.base_settings_main_cpy
     And having:
     | name                              | value                        |
     | group_light_multi_company         | True                         |
     | module_inter_company_rules        | True                         |
     | company_share_partner             | False                        |
   Then execute the setup

  @sale_pricelist
  Scenario:
  Given I need a "sale.config.settings" with oid: scen.sale_settings_main_cpy
     And having:
     | name                              | value                        |
     | sale_pricelist_setting            | formula                      |
     | group_sale_pricelist              | True                         |
     | group_pricelist_item              | True                         |
   Then execute the setup
