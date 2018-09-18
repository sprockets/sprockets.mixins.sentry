sprockets.mixins.sentry
=======================
A RequestHandler mixin for sending exceptions to Sentry

|Version| |Downloads| |Status| |Coverage| |License|

Installation
------------
``sprockets.mixins.sentry`` is available on the
`Python Package Index <https://pypi.python.org/pypi/sprockets.mixins.sentry>`_
and can be installed via ``pip`` or ``easy_install``:

.. code-block:: bash

   pip install sprockets.mixins.sentry

Requirements
------------
- `raven`_
- `tornado`_

API Documentation
-----------------
.. automodule:: sprockets.mixins.sentry
   :members:

Examples
--------
The following application will report errors to sentry if you export the
:envvar:`SENTRY_DSN` environment variable and make a request to
http://localhost:8000/whatever provided that *whatever* is not an integer.

.. literalinclude:: example.py

Version History
---------------

* `1.2.0`_

  - Extend raven pin so that we can use python 3.7
  - Advertise python 3.7 support
  - Drop python 3.4 from support matrix
  - Remove unused import of urllib.parse

* `1.1.2`_

  - Add email sanitization processor

* `1.1.1`_

  - Fix password scrubbing in URLs.
  - Remove support for python 2.6, 3.2, and 3.3

* `1.1.0`_

  - Move raven client initialization into ``sprockets.mixins.sentry.install``
  - Add support for setting raven.Client options when calling ``install`` on
    the application.
  - The sentry "environment" is set to the ``$ENVIRONMENT`` environment
    variable if it is set.

* `1.0.0`_

  - Work around `getsentry/raven-python#735`_

.. _getsentry/raven-python#735: https://github.com/getsentry/raven-python/issues/735

* `0.4.0`_ (16-Dec-2015)

  - Ignore web.Finish exceptions

* `0.3.0`_ (13-Jul-2015)

  - Add ``sprockets.mixins.sentry.SentryMixin.sentry_extra``
  - Add ``sprockets.mixins.sentry.SentryMixin.sentry_tags``
  - Improve module reporting in Sentry messages
  - Improved documentation

* `0.2.0`_ (22-Jun-2015)

  - Stop reporting :class:`tornado.web.HTTPError`

* `0.1.0`_ (13-May-2015)

  - Initial public release

Issues
------
Please report any issues to the Github project at `https://github.com/sprockets/sprockets.mixins.sentry/issues <https://github.com/sprockets/sprockets.mixins.sentry/issues>`_

Source
------
``sprockets.mixins.sentry`` source is available on Github at `https://github.com/sprockets/sprockets.mixins.sentry <https://github.com/sprockets/sprockets.mixins.sentry>`_

License
-------
``sprockets.mixins.sentry`` is released under the `3-Clause BSD license <https://github.com/sprockets/sprockets.mixins.sentry/blob/master/LICENSE>`_.

.. _raven: https://raven.readthedocs.org/
.. _tornado: https://tornadoweb.org/

.. _0.1.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/e01c264...0.1.0
.. _0.2.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.1.0...0.2.0
.. _0.3.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.2.0...0.3.0
.. _0.4.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.3.0...0.4.0
.. _1.0.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.4.0...1.0.0
.. _1.1.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.0.0...1.1.0
.. _1.1.1: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.1.0...1.1.1
.. _1.1.2: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.1.1...1.1.2
.. _1.2.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.1.2...1.2.0
.. _Next Release: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.2.0...HEAD

.. |Version| image:: https://badge.fury.io/py/sprockets.mixins.sentry.svg?
   :target: http://badge.fury.io/py/sprockets.mixins.sentry

.. |Status| image:: https://travis-ci.org/sprockets/sprockets.mixins.sentry.svg?branch=master
   :target: https://travis-ci.org/sprockets/sprockets.mixins.sentry

.. |Coverage| image:: https://img.shields.io/coveralls/sprockets/sprockets.mixins.sentry.svg?
   :target: https://coveralls.io/r/sprockets/sprockets.mixins.sentry

.. |Downloads| image:: https://pypip.in/d/sprockets.mixins.sentry/badge.svg?
   :target: https://pypi.python.org/pypi/sprockets.mixins.sentry

.. |License| image:: https://pypip.in/license/sprockets.mixins.sentry/badge.svg?
   :target: https://sprocketsmixinssentry.readthedocs.org

