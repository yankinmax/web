# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @modules_up
  Scenario: install modules
    Given I install the required modules with dependencies
        | name                     |
        # oca/ocb
        | account                  |
        | sale                     |
        | crm                      |
        | survey                   |
        | web_easy_switch_company  |
        # OCA/server-tools
        # | disable_openerp_online
        # OCA/l10n-france
        | l10n_fr_siret            |
        # OCA/partner-contact
        | partner_firstname        |
        # OCA/web
        | web_duplicate_visibility |
        # OCA/survey
        | partner_survey           |
        # OCA/connector-telephony
        | base_phone               |
        # local-src
        | report_page_endnote      |
        | fields_regex_validation  |
        | specific_base            |
