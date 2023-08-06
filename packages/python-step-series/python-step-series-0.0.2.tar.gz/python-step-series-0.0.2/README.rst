.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://img.shields.io/github/contributors/ponoor/python-step-series.svg?style=for-the-badge
    :alt: Contributors: N/A
    :target: https://github.com/ponoor/python-step-series
.. image:: https://img.shields.io/github/forks/ponoor/python-step-series.svg?style=for-the-badge
    :alt: Forks: N/A
    :target: https://github.com/ponoor/python-step-series/network/members
.. image:: https://img.shields.io/github/stars/ponoor/python-step-series.svg?style=for-the-badge
    :alt: Stars: N/A
    :target: https://github.com/ponoor/python-step-series/stargazers
.. image:: https://img.shields.io/github/issues/ponoor/python-step-series.svg?style=for-the-badge
    :alt: Issues: N/A
    :target: https://github.com/ponoor/python-step-series/issues
.. image:: https://img.shields.io/github/license/ponoor/python-step-series.svg?style=for-the-badge
    :alt: License: MIT
    :target: https://github.com/ponoor/python-step-series/blob/main/LICENSE.txt


==================
python-step-series
==================


    A Python library for OSC communication with the Ponoor Step-series devices.


Welcome to ``python-step-series``, a Python library to stupidly simplify communication
with ponoor's Step-series devices.

To get started, follow the simple example below and read the `documentation`_ to truly
see what the Step-series devices have to offer.


Installation
============

There are multiple ways to install ``python-step-series``. The easiest way is from PyPI:

.. code-block:: shell

    pip install python-step-series

Or you can install from source. See the `Contributing`_ guide for more information
on how to do that.

``python-step-series`` requires Python >=3.7.

First-steps Example
===================

.. code-block:: python

    from stepseries.commands import GetVersion, SetDestIP
    from stepseries.step400 import STEP400
    from stepseries.responses import OSCResponse, Version

    def default_handler(message: OSCResponse) -> None:
        print("Message received:", message)

    def version_handler(message: Version) -> None:
        print("Firmware:")
        print(" - Name:", message.firmware_name)
        print(" - Version:", message.firmware_version)
        print(" - Compiled:", message.compile_date)

    if __name__ == '__main__':
        # Configurations that should be changed
        dip_switch_id = 0  # Should match what is set on the device
        local_ip_address = "10.1.21.56"  # The ip address of the device
        local_port = 50000
        server_address = "0.0.0.0"  # The address of the server; should always be 0.0.0.0 (the local machine)
        server_port = 50100

        # Create a device instance using the configurations above
        # This does two things: creates a communication interface and starts up an OSC endpoint for
        # the device to communicate with
        device = STEP400(dip_switch_id, local_ip_address, local_port, server_address, server_port)

        # Register a default handler for messages
        # Typically, these are used to log events and print to stdout
        # It is recommended to instead register 'filtered' handlers if
        # you want to parse the message (like the one below)
        device.on(None, default_handler)

        # Register a handler just for version info
        device.on(Version, version_handler)

        # Enable communication with the device
        device.set(SetDestIP())

        # Get the current version of the firmware
        version: Version = device.get(GetVersion())


Commands & Responses
====================

`python-step-series` does its best to maintain a simple, yet intuitive API interface
regardless of a developer's experience level. As an example, the library provides a
template for each command in a nice `dataclass` object. So, instead of writing

.. code-block:: python

    device.set("/setBemfParam 2 1500 200 127 43")

which might be prone to typing errors like mispelling or putting a
parameter in the wrong spot, you instead write

.. code-block:: python

    from stepseries.commands import SetBemfParam

    device.set(
        SetBemfParam(
            motorID=2,
            INT_SPEED=1500,
            ST_SLP=200,
            FN_SLP_ACC=127,
            FN_SLP_DEC=43
        )
    )

Also, the library will convert the response from the device into a usable
`dataclass` object. For example, instead of a raw string response like

.. code-block:: python

    from stepseries.commands import GetBemfParam

    resp = device.get(GetBemfParam(1))
    print(resp)

    >>> /bemfParam 1 1032 25 41 41

which you will then have to later interpolate, you will instead receive a
response like

.. code-block:: python

    from stepseries.commands import GetBemfParam
    from stepseries.responses import BemfParam

    resp: BemfParam = device.get(GetBemfParam(1))
    print(resp.INT_SPEED)
    print(resp.FN_SLP_ACC)
    print(resp)

    >>> 1032
    >>> 41
    >>> BemfParam(motorID=1, INT_SPEED=1032, ST_SLP=25, FN_SLP_ACC=41, FN_SLP_DEC=41)

where all the interpolation has already been completed for you.


Making Changes & Contributing
=============================

Any ideas on how to improve this library are welcome. Please see the `Contributing`_ guide for
a full run-down on how to contribute to this project as well as some tips for
making sure your idea is added.

We thank you in-advance for your contributions.

Note
====

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.


.. TODO: Point link at RTD
.. _documentation: https://ponoor.com/en/docs/step-series/
.. _Contributing: https://github.com/ponoor/python-step-series/blob/main/CONTRIBUTING.rst
