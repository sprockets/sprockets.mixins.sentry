import sys
import signal

from tornado import ioloop, web

from sprockets.mixins import sentry


class Handler(sentry.SentryMixin, web.RequestHandler):

    def initialize(self, **kwargs):
        tags = kwargs.pop('tags', dict())
        super().initialize(**kwargs)
        self.sentry_tags.update(tags)

    def get(self, status_code):
        self.set_status(int(status_code))


def make_application(app_tags):
    application = web.Application([(r'/(\S+)', Handler)])
    sentry.install(application, include_paths=[__name__], tags=app_tags)
    return application


def stop(signo, frame):
    iol = ioloop.IOLoop.current()
    iol.add_callback_from_signal(iol.stop)


if __name__ == '__main__':
    app_tags = {}
    for arg in sys.argv[1:]:
        name, _, value = arg.partition('=')
        app_tags[name] = value

    signal.signal(signal.SIGINT, stop)
    app = make_application(app_tags)
    app.listen(8000)
    ioloop.IOLoop.current().start()
