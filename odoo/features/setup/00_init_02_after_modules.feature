# -*- coding: utf-8 -*-
@depiltech @setup_after_modules

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @company
  Scenario: SETUP company informations
    Given I need a "res.company" with oid: base.main_company
    And having
       | key        | value              |
       | country_id | by oid: base.fr    |

  @company
  Scenario: Configure main partner and company
  Given I need a "res.partner" with oid: scenario.user_agencyHolding_res_partner
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
  Given I need a "res.company" with oid: scenario.company_agencyHolding
    And having:
      | key                | value                               |
      | name               | Agencies Holding                    |
      | street             |                                     |
      | street2            |                                     |
      | zip                |                                     |
      | city               |                                     |
      | country_id         | by code: FR                         |
      | phone              | +33 00 000 00 00                    |
      | fax                | +33 00 000 00 00                    |
      | website            |                                     |
      | currency_id        | by name: EUR                        |
      | can_create_product | True                                |
      | partner_id         | by oid: scenario.user_agencyHolding_res_partner |
      | parent_id          | by oid: base.main_company           |

  @mail @outgoing @mailtrap
  Scenario: Create the outgoing mail server
    Given I need a "ir.mail_server" with oid: scenario.mailtrapio1
    And having:
    | name            | value             |
    | name            | mailtrapio1       |
    | sequence        | 1                 |
