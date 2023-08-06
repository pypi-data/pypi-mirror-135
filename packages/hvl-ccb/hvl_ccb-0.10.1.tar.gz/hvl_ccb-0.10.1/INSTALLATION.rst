============
Installation
============


Stable release
--------------

To install HVL Common Code Base, run this command in your terminal:

.. code-block:: console

    $ pip install hvl_ccb

To install HVL Common Code Base with optional Python libraries that require manual
installations of additional system libraries, you need to specify on installation
extra requirements corresponding to these controllers. For instance, to install
Python requirements for LabJack and TiePie devices, run:

.. code-block:: console

    $ pip install "hvl_ccb[tiepie,labjack]"

See below for the info about additional system libraries and the corresponding extra
requirements.

To install all extra requirements run:

.. code-block:: console

    $ pip install "hvl_ccb[all]"

This is the preferred method to install HVL Common Code Base, as it will always install
the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for HVL Common Code Base can be downloaded from the `GitLab repo`_.

You can either clone the repository:

.. code-block:: console

    $ git clone git@gitlab.com:ethz_hvl/hvl_ccb.git

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://gitlab.com/ethz_hvl/hvl_ccb/-/archive/master/hvl_ccb.tar.gz

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .


.. _GitLab repo: https://gitlab.com/ethz_hvl/hvl_ccb
.. _tarball: https://gitlab.com/ethz_hvl/hvl_ccb/-/archive/master/hvl_ccb.tar.gz


Additional system libraries
---------------------------

If you have installed `hvl_ccb` with any of the extra features corresponding to
device controllers, you must additionally install respective system library; these are:

+-------------------------+------------------------------------------------------------+
| Extra feature           | Additional system library                                  |
+=========================+============================================================+
| :code:`labjack`         | `LJM Library`_                                             |
+-------------------------+------------------------------------------------------------+
| :code:`picotech`        | `PicoSDK`_ (Windows) / `libusbpt104`_ (Ubuntu/Debian)      |
+-------------------------+------------------------------------------------------------+
| :code:`tiepie`          | `LibTiePie SDK`_                                           |
+-------------------------+------------------------------------------------------------+

For more details on installation of the libraries see docstrings of the corresponding
:code:`hvl_ccb` modules.

.. _`LibTiePie SDK`: https://www.tiepie.com/en/libtiepie-sdk
.. _`libusbpt104`: https://labs.picotech.com/debian/pool/main/libu/libusbpt104/
.. _`LJM Library`: https://labjack.com/ljm
.. _`PicoSDK`: https://www.picotech.com/downloads
