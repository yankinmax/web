FROM camptocamp/odoo-project:9.0
MAINTAINER Camptocamp

# Install additional debian packages if needed
# RUN set -x; \
#         apt-get update \
#         && apt-get install -y --no-install-recommends \
#         python-shapely \
#         && apt-get clean \
#         && rm -rf /var/lib/apt/lists/*

# Install additional python packages if needed
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

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
  /opt/odoo/external-src/connector-telephony, \
  /opt/odoo/external-src/partner-contact"
