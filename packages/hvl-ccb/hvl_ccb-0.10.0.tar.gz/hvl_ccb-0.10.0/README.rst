====================
HVL Common Code Base
====================

.. image:: https://img.shields.io/pypi/v/hvl_ccb?logo=PyPi
   :target: https://pypi.org/project/hvl_ccb/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/hvl_ccb?logo=Python
   :target: https://pypi.org/project/hvl_ccb/
   :alt: Supported Python versions

.. image:: https://img.shields.io/gitlab/pipeline/ethz_hvl/hvl_ccb/master?logo=gitlab
    :target: https://gitlab.com/ethz_hvl/hvl_ccb/-/tree/master
    :alt: Pipeline status

.. image:: https://img.shields.io/gitlab/coverage/ethz_hvl/hvl_ccb/master?logo=gitlab
    :target: https://gitlab.com/ethz_hvl/hvl_ccb/commits/master
    :alt: Coverage report

.. image:: https://img.shields.io/readthedocs/hvl_ccb?logo=read-the-docs
    :target: https://hvl-ccb.readthedocs.io/en/stable/
    :alt: Documentation Status

.. image:: https://img.shields.io/gitlab/pipeline/ethz_hvl/hvl_ccb/devel?label=devel&logo=gitlab
    :target: https://gitlab.com/ethz_hvl/hvl_ccb/-/tree/devel
    :alt: Development pipeline status

Python common code base (CCB) to control devices, which are used in high-voltage
research. All implemented devices are used and tested in the High Voltage Laboratory
(`HVL`_) of the Federal Institute of Technology Zurich (ETH Zurich).

* Free software: GNU General Public License v3
* Copyright (c) 2019-2022 ETH Zurich, SIS ID and HVL D-ITET

.. _`HVL`: https://hvl.ee.ethz.ch/

Features
--------

For managing multi-device experiments instantiate the :code:`ExperimentManager`
utility class.

Devices
~~~~~~~

The device wrappers in :code:`hvl_ccb` provide a standardised API with configuration
dataclasses, various settings and options, as well as start/stop methods.
Currently wrappers are available to control the following devices:

+-------------------------+------------------------------------------------------------+
| Function/Type           | Devices                                                    |
+=========================+============================================================+
| Data acquisition        | | LabJack (T4, T7, T7-PRO; requires `LJM Library`_)        |
|                         | | Pico Technology PT-104 Platinum Resistance Data Logger   |
|                         |   (requires `PicoSDK`_/`libusbpt104`_)                     |
+-------------------------+------------------------------------------------------------+
| Digital Delay Generator | | Highland T560                                            |
+-------------------------+------------------------------------------------------------+
| Digital IO              | | LabJack (T4, T7, T7-PRO; requires `LJM Library`_)        |
+-------------------------+------------------------------------------------------------+
| Experiment control      | | HVL Cube with and without Power Inverter                 |
+-------------------------+------------------------------------------------------------+
| Gas Analyser            | | MBW 973-SF6 gas dew point mirror analyzer                |
|                         | | Pfeiffer Vacuum TPG (25x, 26x and 36x) controller for    |
|                         |   compact pressure gauges                                  |
|                         | | SST Luminox oxygen sensor                                |
+-------------------------+------------------------------------------------------------+
| I2C host                | | TiePie (HS5, WS5; requires `LibTiePie SDK`_)             |
+-------------------------+------------------------------------------------------------+
| Laser                   | | CryLaS pulsed laser                                      |
|                         | | CryLaS laser attenuator                                  |
+-------------------------+------------------------------------------------------------+
| Oscilloscope            | | Rhode & Schwarz RTO 1024                                 |
|                         | | TiePie (HS5, HS6, WS5; requires `LibTiePie SDK`_)        |
+-------------------------+------------------------------------------------------------+
| Power supply            | | Elektro-Automatik PSI9000                                |
|                         | | FuG Elektronik                                           |
|                         | | Heinzinger PNC                                           |
|                         | | Technix capacitor charger                                |
+-------------------------+------------------------------------------------------------+
| Stepper motor drive     | | Newport SMC100PP                                         |
|                         | | Schneider Electric ILS2T                                 |
+-------------------------+------------------------------------------------------------+
| Temperature control     | | Lauda PRO RP 245 E circulation thermostat                |
+-------------------------+------------------------------------------------------------+
| Waveform generator      | | TiePie (HS5, WS5; requires `LibTiePie SDK`_)             |
+-------------------------+------------------------------------------------------------+

Each device uses at least one standardised communication protocol wrapper.

Communication protocols
~~~~~~~~~~~~~~~~~~~~~~~

In :code:`hvl_ccb` by "communication protocol" we mean different levels of
communication standards, from the low level actual communication protocols like
serial communication to application level interfaces like VISA TCP standard. There
are also devices in :code:`hvl_ccb` that use a dummy communication protocol;
this is because these devices are build on proprietary manufacturer libraries that
communicate with the corresponding devices, as in the case of TiePie or LabJack devices.

The communication protocol wrappers in :code:`hvl_ccb` provide a standardised API with
configuration dataclasses, as well as open/close and read/write/query methods.
Currently, wrappers for the following communication protocols are available:

+------------------------+-------------------------------------------------------------+
| Communication protocol | Devices using                                               |
+========================+=============================================================+
| Modbus TCP             | | Schneider Electric ILS2T stepper motor drive              |
+------------------------+-------------------------------------------------------------+
| OPC UA                 | | HVL Cube with and without Power Inverter                  |
+------------------------+-------------------------------------------------------------+
| Serial                 | | CryLaS pulsed laser and laser attenuator                  |
|                        | | FuG Elektronik power supply (e.g. capacitor charger HCK)  |
|                        |   using the Probus V protocol                               |
|                        | | Heinzinger PNC power supply                               |
|                        |   using Heinzinger Digital Interface I/II                   |
|                        | | SST Luminox oxygen sensor                                 |
|                        | | MBW 973-SF6 gas dew point mirror analyzer                 |
|                        | | Newport SMC100PP single axis driver for 2-phase stepper   |
|                        |   motors                                                    |
|                        | | Pfeiffer Vacuum TPG (25x, 26x and 36x) controller for     |
|                        |   compact pressure gauges                                   |
|                        | | Technix capacitor charger                                 |
+------------------------+-------------------------------------------------------------+
| TCP                    | | Lauda PRO RP 245 E circulation thermostat                 |
+------------------------+-------------------------------------------------------------+
| Telnet                 | | Technix capacitor charger                                 |
+------------------------+-------------------------------------------------------------+
| VISA TCP               | | Elektro-Automatik PSI9000 DC power supply                 |
|                        | | Rhode & Schwarz RTO 1024 oscilloscope                     |
+------------------------+-------------------------------------------------------------+
| *propriety*            | | LabJack (T4, T7, T7-PRO) devices, which communicate via   |
|                        |   `LJM Library`_                                            |
|                        | | Pico Technology PT-104 Platinum Resistance Data Logger,   |
|                        |   which communicate via `PicoSDK`_/`libusbpt104`_           |
|                        | | TiePie (HS5, HS6, WS5) oscilloscopes, generators and I2C  |
|                        |   hosts, which communicate via `LibTiePie SDK`_             |
+------------------------+-------------------------------------------------------------+

.. _`LibTiePie SDK`: https://www.tiepie.com/en/libtiepie-sdk
.. _`libusbpt104`: https://labs.picotech.com/debian/pool/main/libu/libusbpt104/
.. _`LJM Library`: https://labjack.com/ljm
.. _`PicoSDK`: https://www.picotech.com/downloads

Sensor and Unit Conversion Utility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Sensor and Unit Conversion Utility is a submodule that allows on the one hand a
unified implementation of hardware-sensors and on the other hand provides a unified
way to convert units. The utility can be used with single numbers (:code:`int`,
:code:`float`) as well as array-like structures containing single numbers
(:code:`np.array()`, :code:`list`, :code:`dict`, :code:`tuple`).

Currently the following sensors are implemented:

- LEM LT 4000S
- LMT 70A

The following unit conversion classes are implemented:

- Temperature (Kelvin, Celsius, Fahrenheit)
- Pressure (Pascal, Bar, Atmosphere, Psi, Torr, Millimeter Mercury)


Documentation
-------------

Note: if you're planning to contribute to the :code:`hvl_ccb` project read
the **Contributing** section in the HVL CCB documentation.

Do either:

* read `HVL CCB documentation at RTD`_,

or

* build and read HVL CCB documentation locally; install first `Graphviz`_ (make sure
  to have the :code:`dot` command in the executable search path) and the Python
  build requirements for documentation::

    $ pip install docs/requirements.txt

  and then either on Windows in Git BASH run::

    $ ./make.sh docs

  or from any other shell with GNU Make installed run::

    $ make docs

  The target index HTML (:code:`"docs/_build/html/index.html"`) should open
  automatically in your Web browser.

.. _`Graphviz`: https://graphviz.org/
.. _`HVL CCB documentation at RTD`: https://readthedocs.org/projects/hvl-ccb/

Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
