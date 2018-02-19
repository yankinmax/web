.. :changelog:

.. Template:

.. 0.0.1 (2016-05-09)
.. ++++++++++++++++++

.. **Features and Improvements**

.. **Bugfixes**

.. **Build**

.. **Documentation**

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

* Update Dockerimage to 10.0-2.4.1
* Update with latest from odoo-template

**Documentation**


10.3.0 (2018-02-15)
+++++++++++++++++++

**Features and Improvements**

* BSMTS-282: Add fields on project project

**Bugfixes**

* Update `base` to fix home menu issue

**Build**

**Documentation**


10.2.0 (2018-02-09)
+++++++++++++++++++

**Features and Improvements**

* Add delivery_slip report: customer reference pulled left and takes
  all page width BSMTS-268
* Add space between addresses in report_invoice BSMTS-270
* Add dots as decimal delimiters for active langs BSMTS-263
* Render tested samples on `project.task` form w/ HTML BSMTS-273

**Bugfixes**

* Fix CKEditor: Remove it after editing is done. BSMTS-265
* Fix substance propagation from SO line to tasks BSMTS-275

  * refactor SO line measure propagation (moved to task)
  * make sure propagation happens only for confirmed SO
  * update substances only if they have no substance measures
  * add tests for the whole SO -> project sync machinery

  Propagation now happens:

  * automatically ONLY on task create
  * manually ONLY via dedicated wizard on the SO

* SO: update analyze sample on lines only when needed


**Build**

* Update odoo-cloud-platform (BIZ-1093)
* Update Project template.


10.1.9 (2018-01-18)
+++++++++++++++++++

**Bugfixes**

* Add InstrId element for BCN restriction in SEPA payment BIZ-1173


10.1.8 (2018-01-16)
+++++++++++++++++++

**Features and Improvements**

* Add ckeditor widget to the test_parameters field in product_template BSMTS-255
* Add updated py3o reports with the new templates BSMTS-256
* Add some space before customer reference in delivery slip report BSMTS-261
* Add project_analysis report: no breaks inside task, task names no longer
  uppercase, only unique legal references BSMTS-252

**Bugfixes**

* Fix groups and missing name on supplier_invoice BSMTS-260
* Remove original `name` field on `account.invoice` form BSMTS-267


10.1.7 (2018-01-09)
+++++++++++++++++++

**Bugfixes**

* Change mail server configuration on production


10.1.6 (2017-12-22)
+++++++++++++++++++

**Features and Improvements**

* Add ckeditor to project, task and product fields


**Bugfixes**

* Fix prod mail conf


10.1.5 (2017-12-21)
+++++++++++++++++++

**Bugfixes**

* Fix mail config password for prod by escaping %



10.1.4 (2017-12-21)
+++++++++++++++++++

**Features and Improvements**

* Add `web_ckeditor4` (from pending PR + improvements)
* Add `mtsmte_web_ckeditor4` for customizations

**Bugfixes**

* Fix terms propagation from sale order BSMTS-244
* Fix for email template translations.
  Forcing the update via song, lang field filled  BSMTS-246


10.1.3 (2017-12-20)
+++++++++++++++++++

**Features and Improvements**

* Imp substance table is now breakable between pages BSMTS-239
* Update sales conditions with translations for MTE and MTS BSMTS-236
* Add prod mail servers BSMTS-208
* Imp Sale order: tasks and substances are properly propagated when
  confirmed order updates BSMTS-158

**Bugfixes**

* Fixed translations for bsmts-234 BSMTS-241

**Bugfixes**

* Fix Sale order: tasks and substances are properly propagated when
  confirmed order updates BSMTS-158
* Fix updated l10n_switzerland to fix a bug BSMTS-242

**Build**

* Raise soft mem limit to 600MB for minion


10.1.2 (2017-12-13)
+++++++++++++++++++

**Features and Improvements**

* Modify analysis report, adding unit on header column on new line
* Add propagation of substances to the sale order from the template BSMTS-224
* IMP analyze_sample in project and sale order is now html BSMTS-233
* ADD analyze_sample from sale order is now propagated to sale.order.line BSMTS-232
* IMP py3o reports now show only date for write_date field BSMTS-237
* Remove Title legal reference when we are on mech_env test BSMTS-238
* Add new email templates for quotations, sale orders, projects and invoices BSMTS-234

**Bugfixes**

* FIX for a recursion bug from BSMTS-211,212

**Build**

* Upgrade docker-compose to 1.17.1

**Documentation**


10.1.1 (2017-12-11)
+++++++++++++++++++

**Features and Improvements**

* Add expiration_date, expiration_respected fields+ filter BSMTS-211
* Add new default tree view for project, tasks and completed tasks fields
  filter on tasks == completed tasks BSMTS-212

**Bugfixes**

* Fix for language support of BSMTS-221,  BSMTS-228
* Fix for project analysis report and BDL, BQL field BSMTS-230
* Fix for customer invoice report BSMTS-226


10.1.0 (2017-11-30)
+++++++++++++++++++

**Features and Improvements**

* Stock picking scrap: update next picking qty BSMTS-197
* Add chatter to project.project BSMTS-219
* Add changes to py3o reports BSMTS-223
* Add project analysis wqeb report changes BSMTS-214
* Add language support to the chemical analysis BSMTS-221
* Renamed conformity field to compliance in product.substance.measure BSMTS-220
* Add changes to management dashboard BSMTS-222
* Add groups to button Invoiceable in project task form BSMTS-225


**Bugfixes**

* Fix product.category data for MT


**Build**

* Remove dummy package
* Replace odoo-prototype w/ odoo-dj latest
* Remove dummy package
* Go for 10.1.0 instead of 10.0.16
* Minion: increase memory limits


10.0.15 (2017-11-27)
++++++++++++++++++++

**Features and Improvements**

* Add BQL field to substance_measure and changes to
  project analysis report BSMTS-186
* Update chemical_review report BSMTS-207
* Remove doc.payment_term_id.note from saleorder report BSMTS-203
* Replaces account_bank_statement_import_camt from Odoo S.A.
  with OCA BSMTS-200
* Add field for vendor bill number BSMTS-201
* Update report quotation request BSMTS-204
* In the invoice report, comment is now displayed as html
  and won't be displayed if empty BSMTS-215
* Changed report logo for the mte company BSMTS-213
* There is no longer default value for comment in
  invoice BSMTS-216
* Add 'tax display' field in sale settings is now B2C BSMTS-217

**Bugfixes**

* Fixed a bug with with creation of product when MTE user BSMTS-206

**Build**

* Replace `account_bank_statement_import_camt` w/ OCA version BSMTS-200
* Remove `web_translate_dialog`


10.0.14 (2017-11-08)
++++++++++++++++++++



**Features and Improvements**

* Added web_translate_dialog module to the migration BSMTS-175
* Product categories are now filtered by company_id via ir.rule BSMTS-178
* "Conform/Not conform" changed to "Compliant/Not compliant" BSMTS-183
* Removed fax number in mts / mte header BSMTS-179
* Project task form changes BSMTS-184
* In quotation report requested_date field is shown when possible
  instead of commitment_date BSMTS-190
* Add sale.order now searchable by customer reference BSMTS-191
* Tasks are now searchable by equipment_id BSMTS-63
* Color in project task calendar is not equipment_d BSMTS-63
* Add hr_attendance
* Changes to project analysis report BSMTS-196
* 'Tax Display' in sales settings are now B2C BSMTS-217

**Bugfixes**

* Py3o now works correctly with empty datefield in project BSMTS-172
* Fix SO line patch: address corner case BSMTS-189


10.0.13 (2017-10-26)
++++++++++++++++++++

**Features and Improvements**

* changed SO QWeb report BSMTS-171
* Updated PO qweb report BSMTS-170
* Update generated songs & xmlid in pre-songs BSMTS-185

**Bugfixes**

* Adding upgrade to an account_payment_mode module as mentioned in BSMTS-174
* FIX account_invoice_rounding bugs in PR

**Build**

* Update Docker image 10.0-2.3.0 -> 10.0-2.4.0
* Clean pending-merges: web,server-tools

**Documentation**


10.0.12 (2017-10-16)
++++++++++++++++++++

**Features and Improvements**

* Changed task.results.sentences list, tree views
  and _rec_name BSMTS-166
* Add generated songs for sale configuration BSMTS-162
* Update OCA/bank-payment BSMTS-165
* Update project analysis QWeb report BSMTS-157
* Task stages now have "final_stage" boolean identification
  was used in the report BSMTS-157
* Updated project py3o report BSMTS-156
* Add conformity field to task and project BSMTS-156
* Made several fields translatable BSMTS-168
* Update base_dj & dj_compilation_stock

**Bugfixes**

* Fixed several warnings in the build BSMTS-254
  1. OCA/project pr to fix uninstallable module
  2. mtsmte_project description added
  3. mtsmte_purchase description added
  4. add 'website_quote' to the mtsmte_sale as it's field was used in onchange
  5. delete empty dummy_test folder
  6. mtsmte_stock description added
  7. deleted useless line from mtsmte_sale test_substance_measure test
  8. made field project_project_id stored

**Build**

**Documentation**


10.0.11 (2017-09-28)
++++++++++++++++++++

**Features and Improvements**

* Install hr_expense BSMTS-153
* Install sale_project_fixed_price_task_completed_invoicing
  through pending-merges BSMTS-153
* Renamed fields in product.substance according to BSMTS-143
* Added field BDL to project_task according to BSMTS-143
* Reformed conformity calculation according to BSMTS-143
* Changed project.task view in order to be able to add
  and change product.substance.measure
* Added help pop ups to fields in product.substance.measure
  and product.substance according to BSMTS-143
* Made purchase.order origin field(Source document) always visible BSMTS-147
* Fields were hidden from project.task and product.template BSMTS-148
* Security rights updated for product.substance.measure BSMTS-151
* Sale order sequences updated according to generated data BSMTS-145
* Users and access data updated according to generated data BSMTS-146
* Add task.results.sentences model and field in project.task BSMTS-149
* Add account_due_list module BSMTS-152
* Add bi_sql_editor and its dependancy module BSMTS-152
* Add Management dashboard in dashboards BSMTS-152

**Bugfixes**

**Build**

**Documentation**


10.0.10 (2017-09-13)
++++++++++++++++++++

**Features and Improvements**

* Update Routes and procurement rules BSMTS-150

**Bugfixes**

**Build**

**Documentation**


10.0.9 (2017-09-07)
+++++++++++++++++++

**Bugfixes**

* SO line preserve substances on create BSMTS-140

  and handle the case where user can add new substances manually.
* [imp] better html formatting for project report BSMTS-103

10.0.8 (2017-09-07)
+++++++++++++++++++

**Features and Improvements**

* Install l10n_ch_payment_slip BSMTS-139
* Install German lang BSMTS-137
* Add followup and translations (`mtsmte_accounting`) BSMTS-138


**Bugfixes**

* SO action_confirm BSMTS-141
* SO line preserve substances on write BSMTS-140
* SO line view: remove `product_substance_ids.comments` BSMTS-140

  When you have comments the whole popup is bloated
  and the UI gets really ugly. Remove the field does the trick.


**Build**

* Upgrade odoo source
* Upgrade server-tools (for `web_environment_ribbon`)
* Remove pending merge for `purchase_discount`

  https://github.com/OCA/purchase-workflow/pull/316



10.0.7 (2017-08-21)
+++++++++++++++++++

**Bugfixes**

* Update stock songs given dj_file BSMTS-136


**Build**

* Add ribbon, clean pending-merges & project.sync
* Latest version of `base_dj`, missing stock settings setup
* Update project from odoo-template


10.0.6 (2017-08-09)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* Update base_dj to latest version
* Missing stock settings setup

**Build**

**Documentation**


10.0.5 (2017-07-31)
+++++++++++++++++++

**Features and Improvements**

* Update odoo user list
* Additional Fields for SO lines/product/substance/mesures/project/tasks
  BSMTS-99
* Add Customer Reference and Reception Date on project (BSMTS-98)
* Update res.partner import BSMTS-95
* Set Currency updates BSMTS-77
* Import date.range BSMTS-126
* Update account settings update code digits BSMTS-109
* Add salesteam to mts BSMTS110
* Import Equipments  BSMTS-115
* Install account_cancel BSMTS-125
* Install web_sheet_full_width BSMTS-121
* Install l10n_ch_pain_credit_transfer & PAIN & Payment mode BSMTS-116
* Tasks: add Deadline field and groupby on tree/search views BSMTS-124
* Add product.substance.line, setting menu & fix so_line view BSMTS-114/113
* Populate the new model Extraction Types BSMTS-117
* Populate the new model Produt method BSMTS-118
* Add stock setup BSMTS-133
* Update COA + journal setup BSMTS-112
* Add products setup BSMTS-72


**Bugfixes**

* Layout in SO and PO. Related to sales_conditions BSMTS105
* Fix so_line errors BSMTS-113

**Build**

* Update to Docker image 10.0-2.3.0
* Use camptocamp/odoo-project:10.0-2.2.0
* Update session_redis to use redis sentinel
* Add entrypoints from odoo-template
* Sync from odoo-template
* Add odoo-prototype and use `base_dj`
* Upgrade odoo source to include security fixes


**Documentation**


10.0.4 (2017-05-17)
+++++++++++++++++++

**Features and Improvements**

* Add purchase_workflow pending merge & install it
* Remove default project_task_type and install the right ones
* Add fields in project and responsibles as followers

**Bugfixes**

* Upgrade odoo source to include `[SEC] ODOO-SA-2017-06-02-1` fix

  See https://github.com/odoo/odoo/issues/17394


**Build**

**Documentation**


10.0.3 (2017-05-05)
+++++++++++++++++++

**Features and Improvements**

* Add 'client_order_ref' in SO Tree view
* Install account_invoice_rounding & account_bank_statement_import_camt
* Activate multi-company features
* Load custom chart of accounts
* Improve loading of users during setup (disable sending of emails)
* Add mailtrap email accounts and production accounts (without usernames)
* Add new module ``mail_company_domain`` allowing to have different alias
  domains per company
* Load warehouses
* Add MT Sales Teams
* Set web_base_url for reports
* Base layout Header for reports of mts/mte
* Fax at company setup for mte

**Build**

* Use camptocamp/odoo-project:10.0-2.1.0


10.0.2 (2017-04-11)
+++++++++++++++++++

**Features and Improvements**

* Install modules maintenance, holidays, account follow-up
* Songs configuration for accounting/sale
* Configure project tasks status
* Add a new py3o report template for projects
* Add substances, configured on products and sales orders, set on tasks

**Build**

* Add possibility to use py3o for reports


10.0.1 (2017-03-31)
+++++++++++++++++++

**Features and Improvements**

* Add demo data
* Update COA for MT

**Bugfixes**

**Build**

**Documentation**
