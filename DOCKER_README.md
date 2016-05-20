It might be difficult to review the diff because many files are just moved around. Here is a guide:

Some things are new:
- `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- the `entrypoint.sh` waits for postgres to come up before running odoo
- the `migrate` is a first version of automatic migration: if there is no database, we run our existing `oerpscenario` scripts

Some things are adapted or just moved around
- python dependencies are installed from debian packages in the `Dockerfile` and/or from `requirements.txt`. We think we'll want both, to use debian packages where available, but allow to run the project without docker just with `virtualenv . ; source bin/activate ; pip install -r requirements.txt `
- the `openerp.cfg` is now static and not a template anymore. This is because docker handles ports and addresses, and we don't want to store any specific configuration in the image anyway.
- the `oerpscenario` wrapper around `behave` for the gherkin scripts is not anymore generated from a template, but static
- the feature of the anybox recipe of creating automatically entry-points for everything is replaced with just setting PYTHONPATH to the odoo directory (it works!)
- odoo is a submodule in `odoo/src`, OCA addons are submodules in `odoo/external-src`, local code is directly committed into `odoo/local-src`
- local gherkin features are in `odoo/features`
- generic debian packages, python dependencies and bin scripts (entrypoint.sh, migrate, oerpscenario, ...) are installed in the base image 'camptocamp/odoo-project'. Additional tools or dependencies can be installed with the local Dockerfile.
