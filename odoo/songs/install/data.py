# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pkg_resources import Requirement
from pkg_resources import resource_stream

import anthem
import codecs

import csv


# csv_unireader and load_csv_stream methods
# will be integrated to anthem common code
# but only at the next release

def csv_unireader(f, encoding="utf-8", **fmtparams):
    data = csv.reader(
        codecs.iterencode(codecs.iterdecode(f, encoding), "utf-8"), **fmtparams
    )
    for row in data:
        yield [e.decode("utf-8") for e in row]


def load_csv_stream(ctx, model_name, data, dialect='excel', encoding='utf-8',
                    **fmtparams):
    """ Load a CSV from a stream
    Usage example::
      from pkg_resources import Requirement, resource_stream
      req = Requirement.parse('my-project')
      load_csv_stream(ctx, 'res.users',
                      resource_stream(req, 'data/users.csv'),
                      delimiter=',')
    """
    data = csv_unireader(data, encoding=encoding, **fmtparams)
    head = data.next()
    values = list(data)
    if values:
        result = ctx.env[model_name].load(head, values)
        ids = result['ids']
        if not ids:
            messages = u'\n'.join(
                u'- %s' % msg for msg in result['messages']
            )
            ctx.log_line(u"Failed to load CSV "
                         u"in '%s'. Details:\n%s" %
                         (model_name, messages))
            raise Exception(u'Could not import CSV. See the logs')
        else:
            ctx.log_line(u"Imported %d records in '%s'" %
                         (len(ids), model_name))


@anthem.log
def import_groups(ctx, req):
    """ Importing groups """
    content = resource_stream(
        req, 'data/install/01.groups.csv'
    )
    load_csv_stream(ctx, 'res.groups', content, delimiter=';')


@anthem.log
def import_partners(ctx, req):
    """ Importing partners """
    content = resource_stream(
        req, 'data/install/02.partners.csv'
    )
    load_csv_stream(ctx, 'res.partner', content, delimiter=';')


@anthem.log
def import_users(ctx, req):
    """ Importing users """
    content = resource_stream(
        req, 'data/install/03.users.csv'
    )
    load_csv_stream(ctx, 'res.users', content, delimiter=';')


@anthem.log
def import_centers(ctx, req):
    """ Importing centers """
    content = resource_stream(
        req, 'data/install/04.centers.csv'
    )
    load_csv_stream(ctx, 'res.company', content, delimiter=';')


@anthem.log
def import_users_dependances(ctx, req):
    """ Importing users dependances """
    content = resource_stream(
        req, 'data/install/05.users_dependances.csv'
    )
    load_csv_stream(ctx, 'res.users', content, delimiter=';')


@anthem.log
def import_centers_dependances(ctx, req):
    """ Importing centers dependances """
    content = resource_stream(
        req, 'data/install/06.centers_dependances.csv'
    )
    load_csv_stream(ctx, 'res.company', content, delimiter=';')


@anthem.log
def import_centers_horaires(ctx, req):
    """ Importing centers horaires """
    content = resource_stream(
        req, 'data/install/07.centers_horaires.csv'
    )
    load_csv_stream(ctx, 'res.company.schedule', content, delimiter=';')


@anthem.log
def import_centers_pts(ctx, req):
    """ Importing centers pts """
    content = resource_stream(
        req, 'data/install/08.centers_pts.csv'
    )
    load_csv_stream(ctx, 'res.company.phototherapist', content, delimiter=';')


@anthem.log
def import_product_all(ctx, req):
    """ Importing product all """
    content = resource_stream(
        req, 'data/install/09.product - all.csv'
    )
    load_csv_stream(ctx, 'product.product', content, delimiter=',')


@anthem.log
def import_product_new(ctx, req):
    """ Importing product new """
    content = resource_stream(
        req, 'data/install/10.product - new.csv'
    )
    load_csv_stream(ctx, 'product.product', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading data """
    req = Requirement.parse('depiltech-odoo')
    import_groups(ctx, req)
    import_partners(ctx, req)
    import_users(ctx, req)
    import_centers(ctx, req)
    import_users_dependances(ctx, req)
    import_centers_dependances(ctx, req)
    import_centers_horaires(ctx, req)
    import_centers_pts(ctx, req)
    import_product_all(ctx, req)
    import_product_new(ctx, req)
