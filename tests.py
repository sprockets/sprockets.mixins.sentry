"""
Tests for the sprockets.mixins.sentry package

"""
from unittest import mock
import os
import sys
import unittest
import uuid

from tornado import testing, web
import pkg_resources
import raven
import tornado

from sprockets.mixins import sentry

# userinfo    = *( unreserved / pct-encoded / sub-delims / ":" )
# unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~"
# pct-encoded = "%" HEXDIG HEXDIG
# sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
#             / "*" / "+" / "," / ";" / "="

VALUES = {'PGSQL_DSN': 'postgres://foo:bar@localhost:5432/dbname',
          'RABBITMQ_DSN': 'amqp://sentry:rabbitmq@localhost:5672/%2f',
          'VIRTUAL_ENV': '/Users/gavinr/Environments/sprockets',
          'PGSQL_SAFE': ("postgres://(-a.1_&!~+*$=;):"
                         "ab.c%1E!$&'(*+,;=)'DEF%40@a/foo?q=12"),
          'PGSQL_BAD': 'postgres://foo:{22.0/7.0~=3.14}@a/b'}
EXPECTATIONS = {'PGSQL_DSN': 'postgres://foo:****@localhost:5432/dbname',
                'RABBITMQ_DSN': 'amqp://sentry:****@localhost:5672/%2f',
                'VIRTUAL_ENV': '/Users/gavinr/Environments/sprockets',
                'PGSQL_SAFE': 'postgres://(-a.1_&!~+*$=;):****@a/foo?q=12',
                'PGSQL_BAD': 'postgres://foo:****@a/b'}

os.environ['SENTRY_DSN'] = (
    'https://00000000000000000000000000000000:'
    '00000000000000000000000000000000@app.getsentry.com/0')


class TestRequestHandler(sentry.SentryMixin, web.RequestHandler):
    send_to_sentry = mock.Mock()

    def initialize(self):
        super().initialize()
        self.sentry_client.send = self.send_to_sentry
        self.send_to_sentry.reset_mock()

    def get(self, action):
        if action == 'fail':
            raise RuntimeError('something unexpected')
        if action == 'http-error':
            raise web.HTTPError(500)
        if action == 'web-finish':
            raise web.Finish()
        if action == 'add-tags':
            self.sentry_tags['some_tag'] = 'some_value'
            raise RuntimeError
        self.set_status(int(action))


class TestDSNPasswordMask(unittest.TestCase):

    def test_password_masking(self):
        x = sentry.SentryMixin()
        x._strip_uri_passwords(VALUES)
        self.assertDictEqual(VALUES, EXPECTATIONS)


class ApplicationTests(testing.AsyncHTTPTestCase):

    def get_app(self):
        self.sentry_client = TestRequestHandler.send_to_sentry
        app = web.Application([(r'/(\S+)', TestRequestHandler)])
        return app

    def get_sentry_message(self):
        if TestRequestHandler.send_to_sentry.called:
            _, _, message = TestRequestHandler.send_to_sentry.mock_calls[0]
            return message
        return None

    def test_that_request_data_is_included(self):
        self.fetch('/fail')
        message = self.get_sentry_message()
        self.assertEqual(message['request']['url'], self.get_url('/fail'))
        self.assertEqual(message['request']['method'], 'GET')
        self.assertEqual(message['request']['data'], '')

    def test_that_extra_data_is_included(self):
        self.fetch('/fail')
        message = self.get_sentry_message()
        extra = message['extra']
        self.assertEqual(
            extra['handler'],
            "'sprockets.mixins.sentry.{0}'".format(
                TestRequestHandler.__name__))

    def test_that_time_spent_is_nonzero(self):
        self.fetch('/fail')
        message = self.get_sentry_message()
        self.assertGreater(int(message['time_spent']), 0)

    def test_that_tags_are_sent(self):
        self.fetch('/add-tags')
        message = self.get_sentry_message()
        self.assertEqual(message['tags']['some_tag'], 'some_value')

    def test_that_modules_are_sent(self):
        self.fetch('/fail')
        message = self.get_sentry_message()
        self.assertEqual(message['modules']['raven'], raven.VERSION)
        self.assertEqual(
            message['modules']['sprockets.mixins.sentry'],
            pkg_resources.get_distribution('sprockets.mixins.sentry').version
        )
        self.assertEqual(message['modules']['sys'], sys.version)
        self.assertEqual(message['modules']['tornado'], tornado.version)

    def test_that_status_codes_are_not_reported(self):
        self.fetch('/400')
        self.assertIsNone(self.get_sentry_message())

    def test_that_http_errors_are_not_reported(self):
        self.fetch('/http-error')
        self.assertIsNone(self.get_sentry_message())

    def test_that_web_finish_is_not_reported(self):
        self.fetch('/web-finish')
        self.assertIsNone(self.get_sentry_message())

    def test_that_tornado_frames_are_captured(self):
        self.fetch('/fail')
        message = self.get_sentry_message()
        exception = message['exception']['values'][0]
        for frame in exception['stacktrace']['frames']:
            if frame['filename'].startswith('tornado'):
                break
        else:
            self.fail('tornado frames not captured in %r' % exception)

    def test_that_tornado_is_not_in_app(self):
        self.fetch('/fail')
        message = self.get_sentry_message()
        exception = message['exception']['values'][0]
        for frame in exception['stacktrace']['frames']:
            if frame['filename'].startswith('tornado'):
                self.assertEqual(frame['in_app'], False)


class InstallationTests(unittest.TestCase):

    # cannot use mock since it answers True to getattr calls
    class Application:
        pass

    def test_that_client_is_installed(self):
        application = self.Application()
        sentry.install(application)
        self.assertIsInstance(application.sentry_client, raven.Client)

    def test_that_client_is_not_installed_unless_dsn_exists(self):
        saved = os.environ.pop('SENTRY_DSN', None)
        try:
            application = self.Application()
            sentry.install(application)
            self.assertIsNone(application.sentry_client)
        finally:
            if saved:
                os.environ['SENTRY_DSN'] = saved

    def test_that_custom_include_paths_are_used(self):
        application = self.Application()
        sentry.install(application, include_paths=['foo'])
        self.assertIn('foo', application.sentry_client.include_paths)
        # the following are hard-coded
        self.assertIn('raven', application.sentry_client.include_paths)
        self.assertIn('sprockets', application.sentry_client.include_paths)
        self.assertIn('sys', application.sentry_client.include_paths)

    def test_that_custom_exclude_paths_are_used(self):
        application = self.Application()
        sentry.install(application, exclude_paths=['foo'])
        self.assertIn('foo', application.sentry_client.exclude_paths)
        # the following are hard-coded
        self.assertIn('raven', application.sentry_client.exclude_paths)
        self.assertIn('sys', application.sentry_client.exclude_paths)
        self.assertIn('tornado', application.sentry_client.exclude_paths)

    def test_that_environment_is_set_by_default(self):
        saved = os.environ.pop('ENVIRONMENT', None)
        try:
            env = str(uuid.uuid4())
            os.environ['ENVIRONMENT'] = env
            application = self.Application()
            sentry.install(application)
            self.assertEqual(application.sentry_client.environment, env)
        finally:
            if saved:
                os.environ['ENVIRONMENT'] = saved


class SanitizeEmailProcessorTests(unittest.TestCase):

    data = {
        'exception': {
            'values': [{
                'stacktrace': {
                    'frames': [{
                        'vars': {
                            'error': 'HTTPError("example@example.com"),',
                            'kwargs': {'email': 'example@example.com'}
                        },
                    }]
                }
            }],
        },
        'request': {
            'data': 'ip_address=1&email=example%40example.com',
            'cookies': {},
            'headers': {'X-Email-Header': 'example+1234@example.net'},
            'query_string': 'email=example@example.com&name=example',
        },
        'extra': {
            'misc': 'Notes for example@example.com',
            'env': {'email': 'example+1234{}@example.com'}
        }
    }

    expectation = {
        'exception': {
            'values': [{
                'stacktrace': {
                    'frames': [{
                        'vars': {
                            'error': 'HTTPError("********"),',
                            'kwargs': {'email': '********'}
                        },
                    }]
                }
            }],
        },
        'request': {
            'data': 'ip_address=1&email=example%40example.com',
            'cookies': {},
            'headers': {'X-Email-Header': '********'},
            'query_string': 'email=********&name=example',
        },
        'extra': {
            'env': {'email': '********'},
            'misc': 'Notes for ********'
        }
    }

    def test_email_is_removed_from_extra_data(self):
        result = sentry.SanitizeEmailsProcessor(mock.Mock()).process(self.data)
        self.assertDictEqual(result, self.expectation)
