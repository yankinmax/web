.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=====================
Multi Company Domains
=====================

Allow to have different email aliases for the different companies.
This module has not been published because it there is no good way
to do that in a safe way. A lof of methods are overriden, and it
should work for the addons used in this project. But installing a new
addon might add a new uncovered path.

Also, there is a limitation for the emails which are received but not accepted,
a bounce email is returned, but we have no way to know which alias domain
should be used for the returning message, so the alias of the user's company
running the fetchmail will be used.

Usage
=====

The alias domains are stored in a new model ``mail.catchall.domain``.
However, there is no menu to configure them: you should edit the parameter
in the normal Settings Parameter menu when you are connected with the company
you want to configure.

Limits
======

There is a lot of places where the domain is used and there no obvious way to
find which domain should be used.

What this module tries to do is:

* if there is a related record (mail.message, ...) and this record has a
  company, then use the domain associated to this company
* if there is no related record or no company on the related record, it
  uses the domain of the company associated to the current user
* for some models which are likely to be used by crons and hence it cannot rely
  on the current user (mail.message, mail.alias), it adds a company_id field
  initialized with the company of the user that creates it

Rejected messages
~~~~~~~~~~~~~~~~~

When an email is received and Odoo tries to find a thread to attach it, it
might reject the email for different reasons (only the followers can answer for
instance). In that case, we don't know which domain should be used. (This is in
``MailThread.message_route_verify`` and
``MailThread._routing_create_bounce_email``).

Parameter group
~~~~~~~~~~~~~~~

There is no possibility to set a group on the configuration parameter
``mail.catchall.domain``.

Installation
~~~~~~~~~~~~

This module better be installed at the initialization of the database.
Because installing it on an existing database will assign the root company
on existing aliases and messages and will wrong their domain aliases.

Notes
=====

All the work is levered by an inherit of ``ir.config_parameter``.  Instead of
writing and reading the value of the key ``mail.catchall.domain``` in the
``ir_config_parameter`` table, it writes it in a new ``mail_catchall_domain``
table alongside the company associated to the domain.  When
``IrConfigParameter.get_param('mail.catchall.domain')`` is called, it will try
to read which domain to use according to keys passed in the context.

All the other inherit ensure that we pass the keys and values expected by
``IrConfigParameter.get_param('mail.catchall.domain')`` in the context.
