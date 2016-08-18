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

  @modules
  Scenario: install modules
    Given I install the required modules with dependencies
        | name                    |
        # oca/ocb
        | account                 |
        | sale                    |
        | crm                     |
        # | survey                  |
        | web_easy_switch_company |
        # OCA/server-tools
        # | disable_openerp_online  |
        | server_environment       |
        | mail_environment         |
        # local-src
        | server_environment_files |

  @mail @outgoing @mailtrap
  Scenario: Create the outgoing mail server
    Given I need a "ir.mail_server" with oid: scenario.mailtrapio1
    And having:
    | name            | value             |
    | name            | mailtrapio1       |
    | sequence        | 1                 |
