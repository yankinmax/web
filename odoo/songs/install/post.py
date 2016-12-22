# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def admin_user_password(ctx):
    # password for the test server,
    # the password must be changed in production
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$12000$utdaq3UuxViLsbaW0jonpA$NI26S.9DH8INhevccSvtF'
        'Sf7.sv6iSjD/0fnsXDHXu51OZOkciNI6AeomyZboTQw30cXduO.4wrYBGHUP95G/Q'
    )


@anthem.log
def main(ctx):
    """ Main """
    admin_user_password(ctx)
