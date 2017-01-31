.. :changelog:

Release History
---------------

Unreleased
++++++++++

**Features and Improvements**

* Add depiltech logo on main company
* Card 97: Configure SMTP outgoing server mail on PROD environment
* Card 206: Configure chart of account for all FR company (only centers)
* Card 217: Add a partner type 'agency customer'

**Bugfixes**

**Build**

**Documentation**


9.9.0 (2017-01-06)
++++++++++++++++++

**Features and Improvements**

* Change admin password at the end of setup
* Update all modules (odoo and oca) at last version
* Card 99: Install module to activate authentication by google account
* Card 216: On payment, set partner and ref even on VAT item entries

**Build**

* Fix log level on integration/prod environments


9.8.0 (2016-12-19)
++++++++++++++++++

**Features and Improvements**

* Clean demo data (and reorganize initial setup)
* Refresh initial data (CSV imports)
* Setup chart of account for all centers (not main companies)
* Delete taxes on products (default taxes will be defined on accounts)
* Create a default warehouse for each company
* Setup company report footer

**Build**

* Update rancher configuration for environments (prod, integration, test)


9.7.0 (2016-12-07)
++++++++++++++++++

**Features and Improvements**

* Card 183: Add discount description on sale order
* Add initial import of groups/partners/company/products

**Bugfixes**

* #188: coach_id related to res.partner instead of res.users.
* Missing translations on program.
* Fix 'required' domain for quantity type in program condition.
* Fix account tax xmlid
* Card 137: Fix group allow to change sale order line price unit


9.6.0 (2016-11-30)
++++++++++++++++++

**Features and Improvements**

* #129: Add specific payment mode module
* #173: Manual discount.
* #161: Quantity is not editable if product has the 'no quantity' flag.
* #174: Discount on specific product + and / or conditions for program


9.5.0 (2016-11-17)
++++++++++++++++++

**Features and Improvements**

* #181: Voucher are linked to sale.order and generated at sale.order confirmation.
* #184: User can select voucher for all center's customer (instead of only quotation customer)
* Disable product popup in sale order lines.
* Create discount program in scenario

**Bugfixes**

* #182: Remove select vouchers when user change the quotation customer.


9.4.0 (2016-11-08)
++++++++++++++++++

**Features and Improvements**

* Program condition: allow to choose quantity computation type.
* Add taxes.

**Bugfixes**

* Fixed product price didn't work when another program defined a pricelist.


9.3.4 (2016-10-27)
++++++++++++++++++

**Features and Improvements**

* Enhance product add action in program.


9.3.3 (2016-10-24)
++++++++++++++++++

**Features and Improvements**

* Product category condition: Manage sub category.
* Update products csv files.

**Bugfixes**

* Condition was not save when type was product category.
* Fix discout program ACL
* Configure report.url settings
* Fix pricelist configuration visibility.


9.3.2 (2016-10-12)
++++++++++++++++++

**Bugfixes**

* RRR fix: Case when we have two discount apply on the same line

**Build**

* Migrate integration database on postgres rds server
* Deployment configuration fixes


9.3.1 (2016-09-30)
++++++++++++++++++

**Features and Improvements**

* Display pricelist for all users
* Product and product category imports
* Discount program acl
* Add product condition in discount program

**Build**

* Rancher migration


9.3.0 (2016-09-20)
++++++++++++++++++

**Features and Improvements**

* Discount Programs and voucher/promo codes.
* Sponsorship management.

**Bugfixes**

* Constraint message is not raw sql error anymore
* Phototherapist required on SO
* Show 'lang' field in contact form
* Show answer to survey


9.2.0 (2016-09-08)
++++++++++++++++++

**Features and Improvements**

* accounting module available


9.1.0 (2016-09-02)
++++++++++++++++++

**Features and Improvements**

* base configuration (16 companies)
* new fields on ``res.company`` object to manage centers extra informations
* new fields on ``res.partner`` object to manage customer specific fields (B2C)
* ``base_phone`` module installed to manage phone number validation and format
* ``fields_regex_validation`` module installed to manage validation of other
  fields like email by PostgreSQL regular expression.
* intercompany rules configuration
* warehouses creation for base companies (16)
* 1 ``admin`` user and 1 ``normal`` user per company/center
* customer diagnostic survey

