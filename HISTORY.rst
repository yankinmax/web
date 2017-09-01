.. :changelog:

Release History
---------------

Unreleased
++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

**Documentation**


10.1.2 (2017-09-01)
+++++++++++++++++++

**Features and Improvements**

* DT-71: Simplify usage of depiltech payment mode
* DT-72: Fix archive restriction on res partner tree view
* DT-75: Custom displaying of pages on partner form view
* DT-73 / DT-77: Custom lead workflow than lead -> opportunity -> customer
* DT-74: Add program_type for each variants of discount program
* DT-79: Fix translations when apply a gift card product in sale order

**Bugfixes**

* Remove export permission on every groups other than Export
* Encode constraint name and message in fields_regex_expression to avoid
  UnicodeDecodeError and display real errors
* Fix unit test on discount_program_report never launched

**Build**

* Drop vouchers created on B2B customers


10.1.1 (2017-08-01)
+++++++++++++++++++

**Bugfixes**

* DT-55: Fix sprint 4:

 * A user can only see product from parents companies
 * Add widget selection on depiltech_payment_mode on sale_order form view
 * Fix translation on sale discount program
 * Configure sale automatic workflow settings
 * Fix 'Early payment discount' on account invoice
 * Create voucher for confirmed sale order only for agency customer
 * Fix Centers can only create agency customer
 * Fix supporting document filename on sale order
 * Fix unlink rights on res partner (Client archivage group)

* DT-56: Fix deletion of partner linked to a company
* DT-57: A conversion of lead create a agency customer
* DT-58: Customize lead/opportunity objects and views
* DT-59: Add planning url field on partner form view
* DT-60: Add center address fields on company


10.1.0 (2017-07-17)
+++++++++++++++++++

**Features and Improvements**

* DT-22: Client view : hide tabs (Contacts Addresses, Sales & Purchases,
  Accounting). And set country by default using company user connected.
* DT-5: Apply same logic for sale tax calculation than on invoices
* DT-17 : Add group to control visibility of archive button on client view
* DT-6: Add early payment discount on customer invoices
* [DT-26] Change the code of the vouchers, random generated not in a sequence
* DT-12: Improve leads in Sales and add a module specific_security
* Hide payment mode field on quotations
* Add field 'This quotation is a gift' on sale.order and account.invoice
* DT-8: Install specific_sale_order module
* DT-7: Add 'Signature bloc' in sale order report
* DT-7: Change the input of promo code on sale order
* DT-7: Custom limit of usage for discount programs
* DT-9: Add a global limit on promo code use
* DT-9: Add a required attachment on sale order when using promo code
* DT-44: Fix the creation of companies for non admin (with group)
* DT-13: Install module discount_program_report
* DT-13/DT-18: Install module discount_program_report
* DT-20: Develop the depiltech payment modes
* DT-44: Fix the creation of companies for non admin (with group)
* DT-11: Add security group for export to csv feature
* DT-10: Add a program condition based on last validated order
* DT-46: Add account payment mode generator wizard

**Bugfixes**

* DT-52: Fix partners rights

**Build**

* Update all repositories


10.0.4 (2017-07-07)
+++++++++++++++++++

**Build**

* Upgrade Docker image to 10.0-2.3.0
* Patch odoo/src with security fixes
* Skip '100_pre-migration-v10' script, because migration done


10.0.3 (2017-06-26)
+++++++++++++++++++

**Build**

* Travis.yml remove docker&docker-compose installation


10.0.2 (2017-06-21)
+++++++++++++++++++

**Bugfixes**

* DT-50: Fix companies rights and pricelist


10.0.1 (2017-06-19)
+++++++++++++++++++

**Bugfixes**

* Fix secure token to minion creation
* DT-39: Fix migration to V10

  * Fix customer invoice form view migration
  * Add migration additional requests before the marabunta migration
  * Add a default value for partner pricelist on partner creation
  * Install sale_automatic_workflow_payment_mode module
  * Define default config parameter in 'discount program' modules
  * DT-44: Fix the creation/updating of companies for non admin

* DT-43: Migration: fix the docker-odoo-project version

**Build**

* Sync with odoo-template
* Update cloud platform addons to use Redis Sentinel


10.0.0 (2017-05-03)
+++++++++++++++++++

**Build**

* DT-27: Migration instance to V10


9.15.0 (2017-03-10)
+++++++++++++++++++

**Features and Improvements**

* DT-1: Change rights on res partner for all users
* Fix domain for discount program


9.14.0 (2017-02-23)
+++++++++++++++++++

**Bugfixes**

* Change res.company _where_calc to allow access rights on inactive companies

**Build**

* Upgrade attachment_s3


9.13.1 (2017-02-07)
+++++++++++++++++++

**Bugfixes**

* Card 193: Fix add specific fields on several models

**Build**

* Add missing environment variable on test instance
* travis - Download Github archive zip files for submodules in order to speed up builds


9.13.0 (2017-02-02)
+++++++++++++++++++

**Features and Improvements**

* Card 193: Add specific fields on several models
* Card 195: Add translatable flag on several fields
* Card 223: Inverse phototherapist and reference fields position on account invoice form view
* Card 237: Add several modules


9.12.0 (2017-02-02)
+++++++++++++++++++

**Bugfixes**

* Remove useless import on install/company.py songs

**Build**

* Migration of instances on cloud-platform


9.10.2 (2017-01-31)
+++++++++++++++++++

**Bugfixes**

* Fix card 97: Configure SMTP outgoing server mail on PROD environment


9.10.1 (2017-01-31)
+++++++++++++++++++

**Bugfixes**

* Add missing pull master before tag


9.10.0 (2017-01-31)
+++++++++++++++++++

**Features and Improvements**

* Add depiltech logo on main company
* Card 97: Configure SMTP outgoing server mail on PROD environment
* Card 206: Configure chart of account for all FR company (only centers)
* Card 217: Add a partner type 'agency customer'


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

