"""
Tests for the sprockets.mixins.sentry package

"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from sprockets.mixins import sentry

VALUES = {'PGSQL_DSN': 'postgres://foo:bar@localhost:5432/dbname',
          'RABBITMQ_DSN': 'amqp://sentry:rabbitmq@localhost:5672/%2f',
          'VIRTUAL_ENV': '/Users/gavinr/Environments/sprockets'}
EXPECTATIONS = {'PGSQL_DSN': 'postgres://foo:****@localhost:5432/dbname',
                'RABBITMQ_DSN': 'amqp://sentry:****@localhost:5672/%2f',
                'VIRTUAL_ENV': '/Users/gavinr/Environments/sprockets'}

class TestDSNPasswordMask(unittest.TestCase):

    def test_password_masking(self):
        x = sentry.SentryMixin()
        result = x._strip_uri_passwords(VALUES)
        self.assertDictEqual(VALUES, EXPECTATIONS)
