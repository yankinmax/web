# -*- coding: utf-8 -*-
@depiltech @setup_before_modules

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

  @report_configuration
  Scenario: setup of program discount config
    Given I need a "ir.config_parameter" with key: report.url
    And having:
      | key   | value                 |
      | key   | report.url            |
      | value | http://localhost:8069 |

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
      | thousands_sep | ,        |
