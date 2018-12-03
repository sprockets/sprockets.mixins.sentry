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
