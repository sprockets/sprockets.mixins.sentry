API
===
.. automodule:: sprockets.mixins.sentry
   :members:

Examples
--------
The following application will report errors to sentry if you export the
:envvar:`SENTRY_DSN` environment variable and make a request to
http://localhost:8000/whatever provided that *whatever* is not an integer.

.. literalinclude:: example.py

.. _raven: https://raven.readthedocs.org/
.. _tornado: https://tornadoweb.org/

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

