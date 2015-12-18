"""
mixins.sentry

A RequestHandler mixin for sending exceptions to Sentry

"""
version_info = (0, 4, 0)
__version__ = '.'.join(str(v) for v in version_info)


import math
import os
import re
import time
try:
    from urllib import parse
except ImportError:
    import urlparse as parse

import raven
from tornado import web

SENTRY_CLIENT = 'sentry_client'
URI_RE = re.compile(r'^[\w\+\-]+://.*:(\w+)@.*')


class SentryMixin(object):
    """
    Report unexpected exceptions to Sentry.

    Mix this in over a :class:`tornado.web.RequestHandler` to report
    unhandled exceptions to Sentry so that you can figure out what
    went wrong.  In order to use this mix-in, all that you have to do
    is define the **SENTRY_DSN** environment variable that contains your
    projects Sentry DSN.  Whenever a request comes it and the environment
    variable is set, this mix-in will create a new :class:`raven.base.Client`
    instance and make it available via the :attr:`sentry_client` property.

    If an exception is caught by :meth:`._handle_request_exception`, then
    it will be reported to Sentry in all it's glory.

    .. attribute:: sentry_client

       The :class:`raven.base.Client` instance or :data:`None` if sentry
       reporting is disabled.  You can modify attributes of the client
       as required for your application -- for example, you can add new
       modules by adding to ``self.sentry_client.include_paths``.

    .. attribute:: sentry_extra

       A :class:`dict` of extra information to pass to sentry when an
       exception is reported.

    .. attribute:: sentry_tags

       A :class:`dict` of tag and value pairs to associated with any
       reported exceptions.

    """

    def __init__(self, *args, **kwargs):
        self.sentry_extra = {}
        self.sentry_tags = {}
        super(SentryMixin, self).__init__(*args, **kwargs)

    def initialize(self):
        sentry_dsn = os.environ.get('SENTRY_DSN')
        if self.sentry_client is None and sentry_dsn:
            modules = ['raven', 'sys', 'tornado', __name__]
            client = raven.Client(sentry_dsn, include_paths=modules)
            setattr(self.application, SENTRY_CLIENT, client)
        super(SentryMixin, self).initialize()

    def _strip_uri_passwords(self, values):
        for key in values.keys():
            matches = URI_RE.search(values[key])
            if matches:
                values[key] = values[key].replace(matches.group(1), '****')
        return values

    def _handle_request_exception(self, e):
        if (isinstance(e, web.HTTPError)
                or isinstance(e, web.Finish)
                or self.sentry_client is None):
            return super(SentryMixin, self)._handle_request_exception(e)

        duration = math.ceil((time.time() - self.request._start_time) * 1000)
        kwargs = {'extra': self.sentry_extra, 'time_spent': duration}
        kwargs['extra'].setdefault(
            'handler', '{0}.{1}'.format(__name__, self.__class__.__name__))
        kwargs['extra'].setdefault('env',
                                   self._strip_uri_passwords(dict(os.environ)))
        if hasattr(self, 'request'):
            kwargs['data'] = {
                'request': {
                    'url': self.request.full_url(),
                    'method': self.request.method,
                    'data': self.request.body,
                    'query_string': self.request.query,
                    'cookies': self.request.headers.get('Cookie', {}),
                    'headers': dict(self.request.headers)},
                'logger': 'sprockets.mixins.sentry'}
            kwargs['extra']['http_host'] = self.request.host
            kwargs['extra']['remote_ip'] = self.request.remote_ip

        if self.sentry_tags:
            kwargs.update({'tags': self.sentry_tags})
        self.sentry_client.captureException(True, **kwargs)

        super(SentryMixin, self)._handle_request_exception(e)

    @property
    def sentry_client(self):
        return getattr(self.application, SENTRY_CLIENT, None)
