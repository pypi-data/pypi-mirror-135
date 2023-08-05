=======
History
=======

0.10.0 (2022-01-17)
-------------------

* Reimplementation of the Cube (before known as Supercube)
* new names:
    * Supercube Typ B -> BaseCube
    * Supercube Typ A -> PICube (power inverter Cube)
* new import:
    * :code:`from hvl_ccb.dev.supercube import SupercubeB` ->
      :code:`from hvl_ccb.dev.cube import BaseCube`
* new programming style:
    * getter / setter methods -> properties
    * e.g. get: :code:`cube.get_support_output(port=1, contact=1)` ->
      :code:`cube.support_1.output_1`
    * e.g. set: :code:`cube.get_support_output(port=1, contact=1,
      state=True)` -> :code:`cube.support_1.output_1 = True`
* unify Exceptions of Cube
* implement Fast Switch-Off of Cube
* remove method :code:`support_output_impulse`
* all active alarms can now be queried :code:`cube.active_alarms()`
* alarms will now result in different logging levels depending on the
  seriousness of the alarm.
* introduction of limits for slope and safety limit for RedReady
* during the startup the CCB will update the time of the cube.
* verification of inputs
* polarity of DC voltage
* Switch from :code:`python-opcua` to :code:`opcua-asyncio`
  (former package is no longer maintained)

0.9.0 (2022-01-07)
------------------

* New device: Highland T560 digital delay and pulse generator over Telnet.
* Rework of the Technix Capacitor Charger.
    * Moved into a separate sub-package
    * NEW import over :code:`import hvl_ccb.dev.technix as XXX`
    * Slightly adapted behaviour
* Add :code:`validate_tcp_port` to validate port number.
* Add :code:`validate_and_resolve_host` to validate and resolve host names and IPs.
    * Remove requirement :code:`IPy`
* Add a unified CCB Exception schema for all devices and communication protocols.
* Add data conversion functions to README.
* Update CI and devel images from Debian 10 buster to Debian 11 bullseye.
* Fix typing due to numpy update.
* Fix incorrect overloading of :code:`clean_values()` in classes of
  type :code:`XCommunicationConfig`.

0.8.5 (2021-11-05)
------------------

* Added arbitrary waveform for TiePie signal generation, configurable via
  :code:`dev.tiepie.generator.TiePieGeneratorConfig.waveform` property.
* In :code:`utils.conversion_sensor`: improvements for class constants; removed SciPy
  dependency.
* Added Python 3.10 support.

0.8.4 (2021-10-22)
------------------

* :code:`utils.validation.validate_number` extension to handle NumPy arrays and
  array-like objects.
* :code:`utils.conversion_unit` utility classes handle correctly :code:`NamedTuple`
  instances.
* :code:`utils.conversion_sensor` and :code:`utils.conversion_unit` code
  simplification (no :code:`transfer_function_order` attribute) and cleanups.
* Fixed incorrect error logging in :code:`configuration.configdataclass`.
* :code:`comm.telnet.TelnetCommunication` tests fixes for local run errors.

0.8.3 (2021-09-27)
------------------

* New data conversion functions in :code:`utils.conversion_sensor` and
  :code:`utils.conversion_unit` modules. Note: to use these functions you must install
  :code:`hvl_ccb` with extra requirement, either :code:`hvl_ccb[conversion]` or
  :code:`hvl_ccb[all]`.
* Improved documentation with respect to installation of external libraries.

0.8.2 (2021-08-27)
------------------

* New functionality in :code:`dev.labjack.LabJack`:
    * configure clock and send timed pulse sequences
    * set DAC/analog output voltage
* Bugfix: ignore random bits sent by to :code:`dev.newport.NewportSMC100PP`
  controller during start-up/powering-up.

0.8.1 (2021-08-13)
------------------

* Add Python version check (min version error; max version warning).
* Daily checks for upstream dependencies compatibility and devel environment
  improvements.

0.8.0 (2021-07-02)
------------------

* TCP communication protocol.
* Lauda PRO RP 245 E circulation thermostat device over TCP.
* Pico Technology PT-104 Platinum Resistance Data Logger device as a wrapper of the
  Python bindings for the PicoSDK.
* In :code:`com.visa.VisaCommunication`: periodic status polling when VISA/TCP keep
  alive connection is not supported by a host.

0.7.1 (2021-06-04)
------------------

* New :code:`utils.validation` submodule with :code:`validate_bool` and
  :code:`validate_number` utilities extracted from internal use within a
  :code:`dev.tiepie` subpackage.
* In :code:`comm.serial.SerialCommunication`:
     * strict encoding errors handling strategy for subclasses,
     * user warning for a low communication timeout value.

0.7.0 (2021-05-25)
------------------

* The :code:`dev.tiepie` module was splitted into a subpackage with, in particular,
  submodules for each of the device types -- :code:`oscilloscope`, :code:`generator`,
  and :code:`i2c` -- and with backward-incompatible direct imports from the submodules.
* In :code:`dev.technix`:
      * fixed communication crash on nested status byte query;
      * added enums for GET and SET register commands.
* Further minor logging improvements: added missing module level logger and removed some
  error logs in :code:`except` blocks used for a flow control.
* In :code:`examples/` folder renamed consistently all the examples.
* In API documentation: fix incorrect links mapping on inheritance diagrams.

0.6.1 (2021-05-08)
------------------

* In :code:`dev.tiepie`:
      * dynamically set oscilloscope's channel limits in
        :code:`OscilloscopeChannelParameterLimits`: :code:`input_range` and
        :code:`trigger_level_abs`, incl. update of latter on each change of
        :code:`input_range` value of a :code:`TiePieOscilloscopeChannelConfig`
        instances;
      * quick fix for opening of combined instruments by disabling
        :code:`OscilloscopeParameterLimits.trigger_delay` (an advanced feature);
      * enable automatic devices detection to be able to find network devices with
        :code:`TiePieOscilloscope.list_devices()`.
* Fix :code:`examples/example_labjack.py`.
* Improved logging: consistently use module level loggers, and always log exception
  tracebacks.
* Improve API documentation: separate pages per modules, each with an inheritance
  diagram as an overview.

0.6.0 (2021-04-23)
------------------

* Technix capacitor charger using either serial connection or Telnet protocol.
* Extensions, improvements and fixes in existing devices:
   * In :code:`dev.tiepie.TiePieOscilloscope`:
       * redesigned measurement start and data collection API, incl. time out
         argument, with no/infinite time out option;
       * trigger allows now a no/infinite time out;
       * record length and trigger level were fixed to accept, respectively, floating
         point and integer numbers;
       * fixed resolution validation bug;
   * :code:`dev.heinzinger.HeinzingerDI` and `dev.rs_rto1024.RTO1024` instances are now
     resilient to multiple :code:`stop()` calls.
   * In :code:`dev.crylas.CryLasLaser`: default configuration timeout and
     polling period were adjusted;
   * Fixed PSI9080 example script.
* Package and source code improvements:
   * Update to backward-incompatible :code:`pyvisa-py>=0.5.2`. Developers, do update
     your local development environments!
   * External libraries, like LibTiePie SDK or LJM Library, are now not installed by
     default; they are now extra installation options.
   * Added Python 3.9 support.
   * Improved number formatting in logs.
   * Typing improvements and fixes for :code:`mypy>=0.800`.

0.5.0 (2020-11-11)
------------------

* TiePie USB oscilloscope, generator and I2C host devices, as a wrapper of the Python
  bindings for the LibTiePie SDK.
* a FuG Elektronik Power Supply (e.g. Capacitor Charger HCK) using the built-in ADDAT
  controller with the Probus V protocol over a serial connection
* All devices poling status or measurements use now a :code:`dev.utils.Poller` utility
  class.
* Extensions and improvements in existing devices:
    * In :code:`dev.rs_rto1024.RTO1024`: added Channel state, scale, range,
      position and offset accessors, and measurements activation and read methods.
    * In :code:`dev.sst_luminox.Luminox`: added querying for all measurements
      in polling mode, and made output mode activation more robust.
    * In :code:`dev.newport.NewportSMC100PP`: an error-prone
      :code:`wait_until_move_finished` method of replaced by a fixed waiting time,
      device operations are now robust to a power supply cut, and device restart is not
      required to apply a start configuration.
* Other minor improvements:
    * Single failure-safe starting and stopping of devices sequenced via
      :code:`dev.base.DeviceSequenceMixin`.
    * Moved :code:`read_text_nonempty` up to :code:`comm.serial.SerialCommunication`.
    * Added development Dockerfile.
    * Updated package and development dependencies: :code:`pymodbus`,
      :code:`pytest-mock`.

0.4.0 (2020-07-16)
------------------

* Significantly improved new Supercube device controller:
    - more robust error-handling,
    - status polling with generic :code:`Poller` helper,
    - messages and status boards.
    - tested with a physical device,
* Improved OPC UA client wrapper, with better error handling, incl. re-tries on
  :code:`concurrent.futures.TimeoutError`.
* SST Luminox Oxygen sensor device controller.
* Backward-incompatible changes:
    - :code:`CommunicationProtocol.access_lock` has changed type from
      :code:`threading.Lock` to :code:`threading.RLock`.
    - :code:`ILS2T.relative_step` and :code:`ILS2T.absolute_position` are now called,
      respectively, :code:`ILS2T.write_relative_step` and
      :code:`ILS2T.write_absolute_position`.
* Minor bugfixes and improvements:
    - fix use of max resolution in :code:`Labjack.set_ain_resolution()`,
    - resolve ILS2T devices relative and absolute position setters race condition,
    - added acoustic horn function in the 2015 Supercube.
* Toolchain changes:
    - add Python 3.8 support,
    - drop pytest-runner support,
    - ensure compatibility with :code:`labjack_ljm` 2019 version library.

0.3.5 (2020-02-18)
------------------

* Fix issue with reading integers from LabJack LJM Library (device's product ID, serial
  number etc.)
* Fix development requirements specification (tox version).

0.3.4 (2019-12-20)
------------------

* New devices using serial connection:
    * Heinzinger Digital Interface I/II and a Heinzinger PNC power supply
    * Q-switched Pulsed Laser and a laser attenuator from CryLas
    * Newport SMC100PP single axis motion controller for 2-phase stepper motors
    * Pfeiffer TPG controller (TPG 25x, TPG 26x and TPG 36x) for Compact pressure Gauges
* PEP 561 compatibility and related corrections for static type checking (now in CI)
* Refactorings:
    * Protected non-thread safe read and write in communication protocols
    * Device sequence mixin: start/stop, add/rm and lookup
    * `.format()` to f-strings
    * more enumerations and a quite some improvements of existing code
* Improved error docstrings (:code:`:raises:` annotations) and extended tests for
  errors.

0.3.3 (2019-05-08)
------------------

* Use PyPI labjack-ljm (no external dependencies)


0.3.2 (2019-05-08)
------------------

* INSTALLATION.rst with LJMPython prerequisite info


0.3.1 (2019-05-02)
------------------

* readthedocs.org support

0.3 (2019-05-02)
----------------

* Prevent an automatic close of VISA connection when not used.
* Rhode & Schwarz RTO 1024 oscilloscope using VISA interface over TCP::INSTR.
* Extended tests incl. messages sent to devices.
* Added Supercube device using an OPC UA client
* Added Supercube 2015 device using an OPC UA client (for interfacing with old system
  version)

0.2.1 (2019-04-01)
------------------

* Fix issue with LJMPython not being installed automatically with setuptools.

0.2.0 (2019-03-31)
------------------

* LabJack LJM Library communication wrapper and LabJack device.
* Modbus TCP communication protocol.
* Schneider Electric ILS2T stepper motor drive device.
* Elektro-Automatik PSI9000 current source device and VISA communication wrapper.
* Separate configuration classes for communication protocols and devices.
* Simple experiment manager class.

0.1.0 (2019-02-06)
------------------

* Communication protocol base and serial communication implementation.
* Device base and MBW973 implementation.
