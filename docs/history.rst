.. :changelog:

Release History
===============

* `2.0.1`_ (15-Mar-2019)

  - Add configuration documentation
  - Include Tornado 6 in pin

* `2.0.0`_ (8-Dec-2018)

  - Add support for Tornado 5
  - Drop Tornado<5 support
  - Drop Python<3.5 support

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

.. _0.1.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/e01c264...0.1.0
.. _0.2.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.1.0...0.2.0
.. _0.3.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.2.0...0.3.0
.. _0.4.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.3.0...0.4.0
.. _1.0.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/0.4.0...1.0.0
.. _1.1.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.0.0...1.1.0
.. _1.1.1: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.1.0...1.1.1
.. _1.1.2: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.1.1...1.1.2
.. _1.2.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.1.2...1.2.0
.. _2.0.0: https://github.com/sprockets/sprockets.mixins.sentry/compare/1.2.0...2.0.0
.. _2.0.1: https://github.com/sprockets/sprockets.mixins.sentry/compare/2.0.0...2.0.1
.. _Next Release: https://github.com/sprockets/sprockets.mixins.sentry/compare/2.0.1...HEAD
