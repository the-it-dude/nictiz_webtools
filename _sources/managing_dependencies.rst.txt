Managing  dependencies
======================

System performs automatic checks on dependecy changes via CI.

Dependencies are split into 4 files: `base`, `dev`, `prod`, `docs` and stored in `app/requirements` folder.

Depency description files can be built, updated and installed using following `make` commands:

 - `make deps` - development
 - `make deps-base` - base dependencies only
 - `make deps-prod` - production dependencies
 - `make deps-dev` - development dependencies
 - `make deps-docs` - documentation dependencies

In order to add new dependency into project - update related file and add new line with `pypi <https://pypi.com>`_ dependency name or git dependency using `-e git+ssh://...` format, then run related `make deps` command.

Every file in `app/requirements/*.in` will be transformed into `pip` compatible `requirements.txt` file and stored with related name in same folder to be later used by docker or make commands for installation purposes.

*ALL* dependencies (development mode)
-------------------------------------

In order to install *all* project dependencies developers can use:

.. code-block::

   make deps

This command will run `make deps-base && make deps-prod && make deps-dev && make deps-docs` sequence.


Base Dependencies
-----------------

Base dependencies contain everything required for normal operation of this project.

Related file: `app/requirements/base.in`

Dependencies can be updated using:

.. code-block::

   make deps-base


Production Dependencies
-----------------------

Production dependencies contain packages related to project deployment (e.g. Sentry integration and Gunicorn webserver).

Dependencies stored in `app/requirements/prod.in`.

File includes base dependencies as Production image is built using `app/requirements/prod.txt`, output from:

.. code-block::

   make deps-prod

Development (excluding documentation)
-------------------------------------

Development dependencies are stored in `app/requirements/dev.in` and contain everything needed for development and debugging of the project.

These dependencies can be updated using:

.. code-block::

   make deps-dev


Documentation only
------------------

Documentation dependencies are residing in `app/requirements/docs.in`
