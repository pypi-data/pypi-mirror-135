plib3.ui Change Log
===================

Version 0.15
------------

- Switch to ``setuputils_build`` PEP 517 build backend.

Version 0.14.2
--------------

- Add ``example`` module that uses the auto-construction facility
  for entry points from ``plib3.stdlib.postinstall`` for the
  example programs shipped with ``plib3.ui``. Remove the
  ``scripts`` source directory since the wrapper scripts for the
  example programs are now auto-constructed as entry points.

Version 0.14.1
--------------

- Fix importing of wrapped example modules from ``plib.stdlib``
  in ``pyidserver-ui3`` and ``scrips-edit3`` example programs.

Version 0.14
------------

- Add ``PImageView`` image view widget.

- Moved basic file open/save functionality into separate
  ``PFileAware`` class.

- Add support for multiple file filters in file open/save dialogs.

- Set parent widget correctly in application file dialogs.

- Add support for passing file names to open on command line
  of notepad and XML viewer example programs.

Version 0.13
------------

- Make ``plib`` an implicit namespace package per PEP 420.

- Update to PEP 517 build compatibility using ``setuputils``
  version 2.0 to build setup.cfg.

Version 0.12.1
--------------

- Update bug fix to correctly handle older PySide2 versions.

Version 0.12
------------

- Fix bug created by Qt5/PySide2 changing ``QSocketNotifier`` to pass
  a ``QSocketDescriptor`` object to notification handlers (instead of
  an ``int`` representing the socket's ``fileno``).

Version 0.11
------------

- Initial release, version numbering continued from ``plib3.gui``.
