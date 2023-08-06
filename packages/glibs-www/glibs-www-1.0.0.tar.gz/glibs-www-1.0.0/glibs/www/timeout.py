"""
This timeout module is useful on deployment environments that implement a timeout on
requests. Usually this timeout is implemented on the HTTP layer, thus we have no
information on runtime (for logging, metrics, etc.) that the request timed out.

What this module does is raise a `DeadlineExceededError` exception so this error can
show up in error aggregators.
"""

import functools
import time

__all__ = ["DeadlineExceededError", "bind_pyramid", "bind_flask"]


class DeadlineExceededError(Exception):
    pass


class _FakeTimer:
    def start(self):
        pass

    def close(self):
        pass


def _timeout(seconds):
    try:
        import gevent

        return gevent.Timeout(seconds, DeadlineExceededError)
    except ImportError:
        return _FakeTimer()


def bind_flask(app):
    timeout_seconds = int(app.config.get("gevent_timeout", "30"))

    def wrap_dispatch_request(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):  # pragma: no cover
            timeout = _timeout(timeout_seconds)
            timeout.start()
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                if time.time() - start_time > timeout_seconds:
                    raise DeadlineExceededError()
                return result
            finally:
                timeout.close()

        return wrapper

    app.dispatch_request = wrap_dispatch_request(app.dispatch_request)


def bind_pyramid(config):
    config.add_tween("glibs.www.timeout.pyramid_tween")


def pyramid_tween(handler, registry):
    timeout_seconds = int(registry.settings.get("gevent_timeout", "30"))

    def request_timeout(request):
        timeout = _timeout(timeout_seconds)
        timeout.start()
        start_time = time.time()
        try:
            result = handler(request)
            if time.time() - start_time > timeout_seconds:
                raise DeadlineExceededError()
            return result
        finally:
            timeout.close()

    return request_timeout
