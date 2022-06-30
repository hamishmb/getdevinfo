Introduction
============

This is GetDevInfo's API documentation. Mostly this documentation is derived from docstrings in the source code, with a few exceptions.

Running GetDevInfo
==================

Calling GetDevInfo from the commandline
---------------------------------------

Run with:

`python3 -m getdevinfo`

.. warning::
    Breaking change: Support for calling with "python3 -m getdevinfo.getdevinfo was removed in v2.0.0.

Calling GetDevInfo from a Python program
----------------------------------------

Run with:

>>>import getdevinfo
>>>getdevinfo.get_info()

.. note::
    For versions prior to v2.0.0, you will need to call with "getdevinfo.getdevinfo.get_info()".

Important: Error reporting in GetDevInfo
========================================

GetDevInfo does not make use of a logger. Instead, GetDevInfo will create the file "/tmp/getdevinfo.errors" when errors occur.

.. note::
    There was no error reporting capability at all for versions before v2.0.0.

.. note::
    If you're running GetDevInfo directly from the commandline, the errors are printed to the standard output instead.

This file should be read, the contents reported or logged, and then the file deleted by programs that are calling GetDevInfo, in order to prevent potential leaking of sensitive disk information.

This is not a major security concern, as it is not expected that sensitive data will be contained in the file in most situations. At worst, a disk UUID or serial number may be present in the file with particular error scenarios.
