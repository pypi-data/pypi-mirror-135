===========
evbus-kafka
===========

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

If wanting to use ``evbus-kafka``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

  pip install evbus-kafka

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com:vmware/idem/evbus-kafka.git
   cd evbus-kafka

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
-----

Configure `pop-evbus <https://gitlab.com/vmware/idem/evbus>`__ for your app.

The ``connection`` portion of the kafka profile accepts any parameters that can be used in
the `AIOKafkaProducer <https://aiokafka.readthedocs.io/en/stable/api.html#aiokafka-producer>`__ class

credentials.yml

.. code-block:: sls

    kafka:
      default:
        connection:
          bootstrap_servers:
            - localhost:9092

Encrypt the credentials file and export the ACCT environment variables

.. code-block:: bash

    $ pip install acct
    $ export ACCT_KEY=$(acct encrypt credentials.yml)
    $ export ACCT_FILE="$PWD/credentials.yml.fernet"


Now when you put a message on the evbus queue, it will be propagated to your configured kafka implementation.

.. code-block:: python

    async def my_func(hub):
        await hub.evbus.broker.put(
            routing_key="channel", body={"message": "event content"}, profile="default"
        )

Testing
=======

A kafka server is necessary for running the tests.
You can use your own kafka server, or you can use `docker <https://docs.docker.com/engine/install/>`__ .
Start a local kafka server:

.. code-block:: bash

    docker run -p 2181:2181 -p 443:9092 -p 9092:9092 \                                    ✔  14s   idem-core 
      --env ADVERTISED_LISTENERS=PLAINTEXT://localhost:443,INTERNAL://localhost:9093 \
      --env LISTENERS=PLAINTEXT://0.0.0.0:9092,INTERNAL://0.0.0.0:9093 \
      --env SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,INTERNAL:PLAINTEXT \
      --env INTER_BROKER=INTERNAL \
      krisgeus/docker-kafka



Configure credentials for testing with a local rabbitmq server:

.. code-block:: sls

    # credentials.yml
    kafka:
      test_development_evbus_kafka:
        connection:
          bootstrap_servers: localhost:9092

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

Reference the `open issues <https://gitlab.com/vmware/idem/evbus-kafka/issues>`__ for a list of
proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
