"""
mixins.sentry

A RequestHandler mixin for sending exceptions to Sentry

"""
version_info = (0, 2, 0)
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

    def __init__(self, *args, **kwargs):
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
        if isinstance(e, web.HTTPError) or self.sentry_client is None:
            return super(SentryMixin, self)._handle_request_exception(e)

        duration = math.ceil((time.time() - self.request._start_time) * 1000)
        kwargs = {
            'extra': {
                'handler': '{0}.{1}'.format(__name__, self.__class__.__name__),
                'env': self._strip_uri_passwords(dict(os.environ))},
            'time_spent': duration}
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
