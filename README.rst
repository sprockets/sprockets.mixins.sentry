DEPRECATED - DO NOT USE

sprockets.mixins.sentry
=======================
A RequestHandler mixin for sending exceptions to Sentry

|Version| |Status| |License|

Installation
------------
``sprockets.mixins.sentry`` is available on the
`Python Package Index <https://pypi.python.org/pypi/sprockets.mixins.sentry>`_
and can be installed via ``pip`` or ``easy_install``:

.. code-block:: bash

   pip install sprockets.mixins.sentry

Documentation
-------------
https://sprocketsmixinssentry.readthedocs.org

Requirements
------------

- `raven <https://raven.readthedocs.org/>`_
- `tornado <https://tornadoweb.org/>`_

Example
-------
This examples demonstrates how to use ``sprockets.mixins.sentry``.

.. code-block:: python

   import raven
   import raven.contrib.tornado
   from tornado import ioloop, web

   class RequestHandler(raven.contrib.tornado.SentryMixin, web.RequestHandler):
       """Requires a ``SENTRY_DSN`` environment variable is set with the
       DSN value provided by sentry.

       The Mixin should catch unhandled exceptions and report them to Sentry.

       """
       def get(self, *args, **kwargs):
           raise ValueError('This should send an error to sentry')

    app = web.Application(
        [('/', RequestHandler)]
    )
    app.sentry_client = raven.Client(
        environment='yourenvironment',
        include_paths=['raven', 'tornado']
    )
    app.listen(8000)
    ioloop.IOLoop.current().start()


Version History
---------------
Available at https://sprocketsmixinssentry.readthedocs.io/en/latest/#version-history

.. |Version| image:: https://img.shields.io/pypi/v/sprockets.mixins.sentry.svg?
   :target: http://badge.fury.io/py/sprockets.mixins.sentry

.. |Status| image:: https://img.shields.io/travis/sprockets/sprockets.mixins.sentry.svg?
   :target: https://travis-ci.org/sprockets/sprockets.mixins.sentry

.. |License| image:: https://img.shields.io/pypi/l/sprockets.mixins.sentry.svg?
   :target: https://sprocketsmixinssentry.readthedocs.org
