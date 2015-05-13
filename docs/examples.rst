Examples
========
The following example demonstrates how to use the sentry mixin.

.. code:: python

    from sprockets.mixins import sentry
    from tornado import ioloop, web

    class RequestHandler(sentry.SentryMixin, web.RequestHandler):
        """Requires a ``SENTRY_DSN`` environment variable is set with the
        DSN value provided by sentry.

        The Mixin should catch unhandled exceptions and report them to Sentry.

        """
        def get(self, *args, **kwargs):
            raise ValueError("This should send an error to sentry")


    application = web.Application([
        (r"/", RequestHandler),
    ])


    if __name__ == "__main__":
        print('Starting')
        application.listen(8080)
        ioloop.IOLoop.instance().start()
