"""
mixins.sentry

A RequestHandler mixin for sending exceptions to Sentry

"""
version_info = (0, 1, 0)
__version__ = '.'.join(str(v) for v in version_info)


import math
import os
import pkg_resources
import raven
import re
import sys
import time
try:
    from urllib import parse
except ImportError:
    import urlparse as parse

SENTRY_CLIENT = 'sentry_client'
URI_RE = re.compile(r'^[\w\+\-]+://.*:(\w+)@.*')


class SentryMixin(object):

    def initialize(self):
        self.sentry_tags = {}
        if not hasattr(self.application, SENTRY_CLIENT):
            sentry_dsn = os.environ.get('SENTRY_DSN')
            if sentry_dsn:
                setattr(self.application, SENTRY_CLIENT,
                        raven.Client(sentry_dsn))
        super(SentryMixin, self).initialize()

    def _strip_uri_passwords(self, values):
        for key in values.keys():
            matches = URI_RE.search(values[key])
            if matches:
                values[key] = values[key].replace(matches.group(1), '****')
        return values

    def _handle_request_exception(self, e):
        if hasattr(self.application, SENTRY_CLIENT):
            duration = math.ceil((time.time() - self.request._start_time) * 1000)
            data = {}
            if hasattr(self, 'request'):
                data = {'request':
                            {'url': self.request.full_url(),
                             'method': self.request.method,
                             'data': self.request.body,
                             'query_string': self.request.query,
                             'cookies': self.request.headers.get('Cookie', {}),
                             'headers': dict(self.request.headers)},
                        'logger': 'sprockets.mixins.sentry'}
            kwargs = {'extra':
                          {'handler': '{0}.{1}'.format(__name__,
                                                       self.__class__.__name__),
                           'env': self._strip_uri_passwords(dict(os.environ)),
                           'http_host': self.request.host,
                           'remote_ip': self.request.remote_ip},
                      'time_spent': duration}
            modules = {}
            for module_name in sys.modules.keys():
                module = sys.modules[module_name]
                if hasattr(module, '__version__'):
                    modules[module_name] = module.__version__
                elif hasattr(module, 'version'):
                    modules[module_name] = module.version
                else:
                    try:
                        modules[module_name] = \
                            pkg_resources.get_distribution(module_name).version
                    except pkg_resources.DistributionNotFound:
                        pass
            data['modules'] = modules
            if self.sentry_tags:
                kwargs.update(self.sentry_tags)
            self.application.sentry_client.captureException(True, data=data,
                                                            **kwargs)
        super(SentryMixin, self)._handle_request_exception(e)
