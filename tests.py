"""
Tests for the sprockets.mixins.sentry package

"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from tornado import testing, web

from sprockets.mixins import sentry

VALUES = {'PGSQL_DSN': 'postgres://foo:bar@localhost:5432/dbname',
          'RABBITMQ_DSN': 'amqp://sentry:rabbitmq@localhost:5672/%2f',
          'VIRTUAL_ENV': '/Users/gavinr/Environments/sprockets'}
EXPECTATIONS = {'PGSQL_DSN': 'postgres://foo:****@localhost:5432/dbname',
                'RABBITMQ_DSN': 'amqp://sentry:****@localhost:5672/%2f',
                'VIRTUAL_ENV': '/Users/gavinr/Environments/sprockets'}


class TestRequestHandler(sentry.SentryMixin, web.RequestHandler):

    def get(self, action):
        if action == 'fail':
            raise RuntimeError('something unexpected')
        if action == 'http-error':
            raise web.HTTPError(500)
        if action == 'add-tags':
            self.sentry_tags['some_tag'] = 'some_value'
            raise RuntimeError
        self.set_status(int(action))
        self.finish()


class TestDSNPasswordMask(unittest.TestCase):

    def test_password_masking(self):
        x = sentry.SentryMixin()
        x._strip_uri_passwords(VALUES)
        self.assertDictEqual(VALUES, EXPECTATIONS)


class ApplicationTests(testing.AsyncHTTPTestCase):

    def get_app(self):
        self.sentry_client = mock.Mock()
        app = web.Application([web.url(r'/(\S+)', TestRequestHandler)])
        setattr(app, sentry.SENTRY_CLIENT, self.sentry_client)
        return app

    def get_call_args(self):
        self.assertTrue(self.sentry_client.captureException.called)
        _, args, kwargs = self.sentry_client.captureException.mock_calls[0]
        return args, kwargs

    def test_that_request_data_is_included(self):
        self.fetch('/fail')
        args, kwargs = self.get_call_args()
        self.assertEqual(args, (True,))

        data = kwargs['data']
        self.assertEqual(data['request']['url'], self.get_url('/fail'))
        self.assertEqual(data['request']['method'], 'GET')
        self.assertEqual(data['request']['data'], b'')

    def test_that_extra_data_is_included(self):
        self.fetch('/fail')
        _, kwargs = self.get_call_args()
        extra = kwargs['extra']
        self.assertEqual(
            extra['handler'],
            'sprockets.mixins.sentry.{0}'.format(TestRequestHandler.__name__))
        self.assertEqual(kwargs['time_spent'], 1)

    def test_that_tags_are_sent(self):
        self.fetch('/add-tags')
        _, kwargs = self.get_call_args()
        self.assertEqual(kwargs['tags']['some_tag'], 'some_value')

    def test_that_status_codes_are_not_reported(self):
        self.fetch('/400')
        self.assertFalse(self.sentry_client.captureException.called)

    def test_that_http_errors_are_not_reported(self):
        self.fetch('/http-error')
        self.assertFalse(self.sentry_client.captureException.called)
