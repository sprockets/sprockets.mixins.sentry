"""
mixins.sentry

A RequestHandler mixin for sending exceptions to Sentry

"""
version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)


import logging
import math
import os
import re
import time
try:
    from urllib import parse
except ImportError:  # pragma no cover
    import urlparse as parse

import raven
from tornado import web


LOGGER = logging.getLogger(__name__)
SENTRY_CLIENT = 'sentry_client'
URI_RE = re.compile(r'^[\w\+\-]+://.*:(\w+)@.*')

_sentry_warning_issued = False


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
        self.sentry_client = None
        self.sentry_extra = {}
        self.sentry_tags = {}
        super(SentryMixin, self).__init__(*args, **kwargs)

    def initialize(self):
        self.sentry_client = get_client(self.application)
        if self.sentry_client is None:
            install(self.application)
            self.sentry_client = get_client(self.application)
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
        self.sentry_client.captureException(**kwargs)

        super(SentryMixin, self)._handle_request_exception(e)


def install(application, **kwargs):
    """
    Call this to install a sentry client into a Tornado application.

    :param tornado.web.Application application: the application to
        install the client into.
    :param kwargs: keyword parameters to pass to the
        :class:`raven.base.Client` initializer.

    :returns: :data:`True` if the client was installed by this call
        and :data:`False` otherwise.

    This function should be called to initialize the Sentry client
    for your application.  It will be called automatically with the
    default parameters by :class:`.SentryMixin` if you do not call
    it during the creation of your application.  You should install
    the client explicitly so that you can set at least the following
    properties:

    - **include_paths** list of python modules to include in tracebacks.
      This function ensures that ``raven``, ``sprockets``, ``sys``, and
      ``tornado`` are included but you probably want to include additional
      packages.

    - **release** the version of the application that is running

    See `the raven documentation`_ for additional information.

    .. _the raven documentation: https://docs.getsentry.com/hosted/clients/
       python/advanced/#client-arguments

    """
    if get_client(application) is not None:
        LOGGER.warning('sentry client is already installed')
        return False

    sentry_dsn = kwargs.pop('dsn', os.environ.get('SENTRY_DSN'))
    if sentry_dsn is None:
        global _sentry_warning_issued
        if not _sentry_warning_issued:
            LOGGER.info('sentry DSN not found, not installing client')
            _sentry_warning_issued = True
        setattr(application, 'sentry_client', None)
        return False

    # ``include_paths`` has two purposes:
    # 1. it tells sentry which parts of the stack trace are considered
    #    part of the application for use in the UI
    # 2. it controls which modules are included in the version dump
    include_paths = set(kwargs.pop('include_paths', []))
    include_paths.update(['raven', 'sprockets', 'sys', 'tornado', __name__])
    kwargs['include_paths'] = list(include_paths)

    # ``exclude_paths`` tells the sentry UI which modules to exclude
    # from the "In App" view of the traceback.
    exclude_paths = set(kwargs.pop('exclude_paths', []))
    exclude_paths.update(['raven', 'sys', 'tornado'])
    kwargs['exclude_paths'] = list(exclude_paths)

    client = raven.Client(sentry_dsn, **kwargs)
    setattr(application, 'sentry_client', client)

    return True


def get_client(application):
    """
    Retrieve the sentry client for `application`.

    :param tornado.web.Application application: application to retrieve
        the sentry client for.
    :returns: a :class:`raven.base.Client` instance or :data:`None`
    :rtype: raven.base.Client

    """
    try:
        return application.sentry_client
    except AttributeError:
        return None
