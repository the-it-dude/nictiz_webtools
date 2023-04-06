Development
===========

This document aims to describe basic development process for the project.

We highly recommend to use pyenv and virtualenv in order to simplify python and dependency management.

Basic development process is following 4 steps:

 1. Install
 2. Write code and Test
 3. Run server (locally or via docker-compose)
 4. Write documentation

Additionally it is possible to update dependencies, see :doc:`managing_dependencies` for details.

Installing project in development mode
--------------------------------------

We're starting project development by installing it's dependencies by running:

.. code-block::

   make install

This command will install development dependencies using `pip`.

Testing
-------

Testing is done using `pytest` utility and can be executed using:

.. code-block::

   make test

This command will run unittest suite for the project.


Running development server (local)
----------------------------------

Development server is useful during development and can be started via:

.. code-block::

   make serve

This will start local python process with dev server in it, available via `http://localhost:8000 <http://localhost:8000>`_.

Note: local development server requires Postgresql and RabbitMQ servers running in order to operate.


Running development server (docker)
-----------------------------------

It is possible to run everything including database, rabbitmq and celery workers together with development server inside docker containers using `docker-compose` and can be done via:

.. code-block::

   make serve-docker

or directly:

.. code-block::

   docker-compose up

NOTE: docker image requires rebuild every time dependencies are updated, therefore `docker-compose stop && docker-compose build && docker-compose up` is necessary.


Writing documentation
---------------------

Documentation is stored inside `docs` folder and presented using `Sphinx` tools.

Files stored in `docs/source/` folder and structured using ReST format.

Documentaion builder dependencies can be installed using:

.. code-block::

   make install-docs

And then documentation itself can be built using

.. code-block::

   make build-docs
