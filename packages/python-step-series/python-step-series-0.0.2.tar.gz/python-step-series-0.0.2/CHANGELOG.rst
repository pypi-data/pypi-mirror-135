=========
Changelog
=========


Development version
===================

Version 0.0.2, 2022-01-21
-------------------------

- Added support for the STEP800 motor controller
- Added the following commands:
    - GetPositionList (``/getPositionList``)
    - GetTval_mA (``/getTval_mA``)
    - GetDir (``/getDir``)
    - EnableDirReport (``/enableDirReport``)
    - SetPositionReportInterval (``/setPositionReportInterval``)
    - SetPositionListReportInterval (``/setPositionListReportInterval``)
    - GetElPos (``/getElPos``)
    - SetElPos (``/setElPos``)
    - ResetDevice (``/resetDevice``)
- Added the ``with_callback`` parameter to ``STEPXXX.get`` to allow users to not send the get response to any registered callbacks
- Added ``response_cls`` to every ``OSCGetCommand`` (NOTE: this attr is now required)
- Added the ``callback`` attr to allow short-hand registration of callbacks for reports (i.e. ``/setPositionReportInterval``)

- Fixed an issue with ``STEPXXX.get`` only returning 1 response when there are multiple (`#1`_)
- Refractored tests to make them more robust and intelligent


Current versions
================

Version 0.0.1, 2021-12-03
-------------------------

- First release


.. _#1: https://github.com/ponoor/python-step-series/issues/1
