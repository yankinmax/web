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

* Changed task.results.sentences list, tree views
  and _rec_name BSMTS-166
* Add generated songs for sale configuration BSMTS-162
* Update OCA/bank-payment BSMTS-165
* Update project analysis QWeb report BSMTS-157
* Task stages now have "final_stage" boolean identification
  was used in the report BSMTS-157

**Bugfixes**

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
