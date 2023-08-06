==========
evbus-pika
==========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

This project contains app-merge components for `pop-evbus <https://gitlab.com/vmware/idem/evbus>`__ .

Getting Started
===============

Prerequisites
-------------

* Python 3.7+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``evbus-pika``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

  pip install evbus-pika

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com:vmware/idem/evbus-pika.git
   cd evbus-pika

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
-----

Configure `pop-evbus <https://gitlab.com/vmware/idem/evbus>`__ for your app.

Create a pika profile

.. code-block:: sls

    pika:
      default:
        connection:
          host: localhost
          port: 5672
          login: guest
          password: guest

Encrypt the credentials file and export the ACCT environment variables

.. code-block:: bash

    $ pip install acct
    $ export ACCT_KEY=$(acct encrypt credentials.yml)
    $ export ACCT_FILE="$PWD/credentials.yml.fernet"


Now when you put a message on the evbus queue, it will be propagated to your configured pika implementation.

.. code-block:: python

    async def my_func(hub):
        await hub.evbus.broker.put(
            routing_key="channel", body={"message": "event content"}, profile="default"
        )

Testing
=======

The rabbitmq-server binary needs to be installed via your package manager.
Start a local rabbitmq-server with the default parameters:

.. code-block:: bash

    sudo rabbitmq-server

Configure credentials for testing with a local rabbitmq server:

.. code-block:: sls

    # credentials.yml
    pika:
      test_development_evbus_pika:
        connection:
          host: localhost
          port: 5672
          login: guest
          password: guest

Encrypt the credentials file and export the ACCT environment variables

.. code-block:: bash

    $ pip install acct
    $ export ACCT_KEY=$(acct encrypt credentials.yml)
    $ export ACCT_FILE="$PWD/credentials.yml.fernet"

Install testing requirements

.. code-block:: bash

    $ pip install -r requirements/test.in

Run the tests with pytest:
.. code-block:: bash

    $ pytest tests


Roadmap
=======

Reference the `open issues <https://gitlab.com/vmware/idem/evbus-pika/issues>`__ for a list of
proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
