.. :changelog:

Release History
---------------

Unreleased
++++++++++

**Features and Improvements**

**Bugfixes**
* Missing translations on program.

**Build**

**Documentation**


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

