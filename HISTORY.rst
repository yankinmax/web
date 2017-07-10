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

* Update odoo user list
* Additional Fields for SO lines/product/substance/mesures/project/tasks
  BSMTS-99
* Add Customer Reference and Reception Date on project (BSMTS-98)
* Update res.partner import BSMTS-95
* Set Currency updates BSMTS-77
* Import date.range BSMTS-126
* Update account settings update code digits BSMTS109
* Add salesteam to mts BSMTS110
* Import Equipments  BSMTS-115
* Install account_cancel BSMTS-125
* Install web_sheet_full_width BSMTS-121

**Bugfixes**

* Layout in SO and PO. Related to sales_conditions BSMTS105

**Build**

* Use camptocamp/odoo-project:10.0-2.2.0
* Update session_redis to use redis sentinel
* Add entrypoints from odoo-template
* Sync from odoo-template

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
