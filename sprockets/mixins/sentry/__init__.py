"""
mixins.sentry

A RequestHandler mixin for sending exceptions to Sentry

"""
import math
import os
import re
import time

from raven.processors import SanitizePasswordsProcessor
import raven
import raven.contrib.tornado

version_info = (1, 2, 0)
__version__ = '.'.join(str(v) for v in version_info)


# This matches the userinfo production from RFC3986 with some extra
# leniancy to account for poorly formed URLs.  For example, it lets
# you include braces and other things in the password section.
URI_RE = re.compile(r"^[\w\+\-]+://"
                    r"[-a-z0-9._~!$&'()*+,;=%]+:"
                    r"([^@]+)"
                    r"@",
                    re.IGNORECASE)


class SanitizeEmailsProcessor(SanitizePasswordsProcessor):
    """
    Remove all email addresses from the payload sent to sentry.

    """

    FIELDS = frozenset(['email', 'email_address'])
    VALUES_RE = re.compile(r"""
    ((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
      (?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|
       \\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")
      @
      (?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]
      (?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|
       [01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|
       [a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|
       \\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))
    """, re.VERBOSE ^ re.IGNORECASE)  # RFC5322

    def sanitize(self, key, value):
        if value is None:
            return

        if isinstance(value, str):
            return self.VALUES_RE.sub(self.MASK, value)

        if not key:  # key can be a NoneType
            return value

        # Just in case we have bytes here, we want to make them into text
        # properly without failing so we can perform our check.
        if isinstance(key, bytes):
            key = key.decode('utf-8', 'replace')
        else:
            key = str(key)

        key = key.lower()
        for field in self.FIELDS:
            if field in key:
                # store mask as a fixed length for security
                return self.MASK
        return value


class SentryMixin(raven.contrib.tornado.SentryMixin):
    """
    Report unexpected exceptions to Sentry.

    Mix this in over a :class:`tornado.web.RequestHandler` to report
    unhandled exceptions to Sentry so that you can figure out what
    went wrong.

    """

    def get_sentry_extra_info(self):
        info = super().get_sentry_extra_info()
        info['extra'].update({
            'env': self._strip_uri_passwords(dict(os.environ)),
            'http_host': self.request.host,
            'remote_ip': self.request.remote_ip
        })
        info['time_spent'] = math.ceil(
            (time.time() - self.request._start_time) * 1000
        )

    @staticmethod
    def _strip_uri_passwords(values):
        for key in values.keys():
            matches = URI_RE.search(values[key])
            if matches:
                values[key] = values[key].replace(matches.group(1), '****')
        return values
