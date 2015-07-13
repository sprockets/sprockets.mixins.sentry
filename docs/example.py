import sys
import signal

from tornado import ioloop, web

from sprockets.mixins import sentry


class Handler(sentry.SentryMixin, web.RequestHandler):

    def initialize(self, **kwargs):
        tags = kwargs.pop('tags', dict())
        super(Handler, self).initialize(**kwargs)
        self.sentry_tags.update(tags)

    def get(self, status_code):
        self.set_status(int(status_code))


def stop(signo, frame):
    iol = ioloop.IOLoop.current()
    iol.add_callback_from_signal(iol.stop)


if __name__ == '__main__':
    tags = {}
    for arg in sys.argv[1:]:
        name, _, value = arg.partition('=')
        tags[name] = value

    signal.signal(signal.SIGINT, stop)
    app = web.Application([web.url(r'/(\S+)', Handler, {'tags': tags})])
    app.listen(8000)
    ioloop.IOLoop.current().start()
