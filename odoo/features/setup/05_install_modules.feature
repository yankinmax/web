# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @modules_up
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
        # local-src
        | report_page_endnote     |
        | fields_regex_validation |
