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
