FROM camptocamp/odoo-project:9.0-1.5.0
MAINTAINER Camptocamp

COPY requirements.txt /opt/odoo/requirements.txt
RUN pip install -r /opt/odoo/requirements.txt

COPY ./features /opt/odoo/features

COPY oerpscenario /opt/odoo/oerpscenario
COPY bin/oerpscenario /opt/odoo/bin/oerpscenario

ENV ADDONS_PATH="/opt/odoo/local-src, \
  /opt/odoo/external-src/enterprise, \
  /opt/odoo/src/addons, \
  /opt/odoo/external-src/server-tools, \
  /opt/odoo/external-src/survey, \
  /opt/odoo/external-src/web, \
  /opt/odoo/external-src/l10n-france, \
  /opt/odoo/external-src/account-financial-reporting, \
  /opt/odoo/external-src/account-financial-tools, \
  /opt/odoo/external-src/bank-payment, \
  /opt/odoo/external-src/bank-statement-import, \
  /opt/odoo/external-src/reporting-engine, \
  /opt/odoo/external-src/sale-workflow, \
  /opt/odoo/external-src/connector-telephony, \
  /opt/odoo/external-src/partner-contact"
