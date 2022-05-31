GetDevInfo(1.1.1)
  * Changes since v1.1.0:

  * Use correct Cygwin package names in README.md.
  * Fix occasional LVM releated crash on Linux.
  * Use get_lv_file_system() as a fallback for when lshw doesn't detect the FS (fixes btrfs and probably others).
  * Improve device detection on Linux (use lsblk as a fallback for more than just NVME disks).
  * Improve error handling in get_file_system().
  * Update setup.py to note addition of Python 3.9 support and removal of Python 3.4 support.

GetDevInfo (1.1.0)
  * Changes since v1.0.10:

  * Add Cygwin support.
  * Avoid shell=True in the compute_block_size() methods.

GetDevInfo (1.0.10)
  * Changes since v1.0.9:

  * Fix a few more NVME-related bugs.
  * Fix a few problems where LVM logical volume and volume group names were swapped.

GetDevInfo (1.0.9)
  * Changes since v1.0.8:

  * Make sure "RawCapacity" key is always a string (sometimes unexpectedly an int).
  * Find NVME disks before LVM disks, fixing crashes.
  * Fix an NVME bug on Fedora with patched lshw that detects NVME disks.
  * No longer return DISKINFO from macos.get_info (unintentional inconsistency).
  * Gather IDs for NVME disks on Linux.
  * Add dependency check for non-Python dependencies in setup.py.
  * Update unit tests.
  * Fix a typo that caused a crash w/ NVME disks under rare circumstances.

GetDevInfo (1.0.8):
  * Changes since v1.0.7:

  * Remove an old fix for Ubuntu 14.04 (no longer supported).
  * Handle bytes to str conversion better on Linux.
  * Generate nicer descriptions for APFS stores, containers, volumes on macOS.
  * Fix lsblk tets on Ubuntu 16.04.
  * Make executable with just 'python3 -m getdevinfo'
  * Update documentation.

GetDevInfo (1.0.7):
  * Changes since v1.0.6:
  *
  * Support detecting NVME disks on Ubuntu 16.04.
  * Remove support for Python 2.
  * Add Python 3.8 to list of supported versions in Python wheel.

GetDevInfo (1.0.6):
  * Changes since v1.0.5:
  *
  * Add support for detecting NVME disks (these don't show up yet in lshw).
  * Add unit tests for methods relating to NVME disks.

GetDevInfo (1.0.5):
  * Changes since v1.0.4:

  * Fix a crash when the vendor string is missing on certain Linux distros.

GetDevInfo (1.0.4):
  * Changes since v1.0.3:

  * Make boot record & boot record strings bytestrings even when unreadable.
  * Clean up the code with pylint.
  * Improve existing Linux unit tests - more throough, esp new tests w/ non-roman characters.
  * Improve existing macOS unit tests - as above.
  * Test non-roman characters in bytestrings as well.
  * Write some tests for get_capabilities & fix a bug.
  * Write some tests for get_partitioning & fix a bug.
  * Write some tests for get_file_system & fix a bug.
  * Write some tests for get_uuid.
  * Write some tests for get_id.
  * Write a test to check info can be gathered without error on the current system.
  * Test coverage with Coverage.py.
  * Update Readme.md to include instructions for running the tests.
  * Fix a bug where extended partitions are given file systems mistakenly.
  * Update API docs to fix some typos.

GetDevInfo (1.0.3):
  * Changes since v1.0.2:

  * Fix blank UUID when not found on Python 3.
  * Change "raw_capacity" key to the intended "RawCapacity" in one place where it was wrong.
  * Make sure boot records and any string found in them are always bytestrings.

GetDevInfo (1.0.2):
  * Changes since 1.0.1:

  * Fix an exception when getting block sizes on Linux with Python 3.
  * Define getdevinfo.getdevinfo.VERSION - useful for users.
  * Bump version to 1.0.2.

GetDevInfo (1.0.1):
  * Changes since v1.0.0:
  *
  * Add unittests from WxFixBoot.
  * Rewrite tests data to obey style guide.
  * Rewrite test functions to obey style guide.
  * Get the unit tests working.
  * Add unittests from DDRescue-GUI.
  * Rewrite the tests to adhere to the style guide.
  * Get the tests working on Linux.
  * Enable platform detection in the unit tests.
  * Get tests working on macOS.
  * Include bytestring workaround for Python 3.
  * Don't use deprecated function plistlib.readPlistFromBytes.
  * Start work on the documentation.
  * Document getdevinfo.py.
  * Document linux.py.
  * Document macos.py.
  * Parse lshw's XML output with LXML, rather than with html.parser (breaks Ubuntu 12.04 support).
  * Remove another workaround for Ubuntu 12.04.
  * Use dd status=none to remove all of dd's output in the boot record strings. (breaks Ubuntu 12.04 support).
  * Don't crash if not run as root on Linux.
  * macOS: get_capacity(): Actually compute human-readable sizes.
  * Fix a RuntimeWarning when running standalone on OS X.
  * macOS: More clearly display whether a drive is removable or not.
  * macOS: is_partition(), remove deprecation warning, but note for internal use only.
  * Start documenting dictionary format.
  * Fix getting IDs under Python 3 on Linux.
  * Finish documenting dictionary format.
  * LVM disks: Set RawCapacity to "Unknown", rather than a human-readable size.
  * Fix more LVM disk stuff under Python 3.
  * Fix several errors with the LVM-related tests,
  * macOS: Fix formatting issues with descriptions.
  * Delayed - can't test on laptop.
  * Update macOS get_capacity() tests to check human-readable capacities too.
  * macOS: Fix issue if Removable key isn't in the plist from diskutil info.
  * Fix for older versions of macOS where the SolidState attribute is missing from the diskutil info plist.
  * Don't require bs4 for testing on macOS.
  * Fix macOS description tests.
  * Fix crashes with unpartitioned disks (Linux).
  * macOS: Fix for disks with more than 9 partitions.
  * macOS: Fix for removable drive detection.
  * Fix unit tests again.
  * Update Readme.md to include build instructions.
  * Update getdevinfo/__init__.py so the wheels work.

GetDevInfo (1.0.0):

  * Create the repository on github.
  * Add the latest GetDevInfo code from WxFixBoot.
  * Begin merging with the code from DDRescue-GUI.
  * More merging.
  * Get it working on Linux.
  * Get it working on macOS.
  * Bring the macOS coding scheme up to date.
  * Obey the python style guide more closely.
  * Remove all of the logging stuff, as it doesn't make sense in a standalone module.
  * Get Python 3 support working on both platforms.
  * Set the version to v1.0.0 and get ready for PyPI.
  * Create setup.py.
  * Fix some import-related issues.
  * Test it again.
  * Release.
