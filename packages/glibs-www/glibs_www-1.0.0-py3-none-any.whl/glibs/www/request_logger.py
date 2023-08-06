import json
import logging

__all__ = ["bind_flask", "bind_pyramid"]

logger = logging.getLogger(__name__)


def bind_flask(app, get_user_id):
    import flask

    def logger():
        try:
            # TODO provide a proper API for this kind of stuff
            if flask.request.path.startswith("/static"):
                return

            user_id = get_user_id()
            if user_id:
                log_request_info(
                    flask.request.path, user_id, flask.request.args.to_dict(flat=False)
                )
        except Exception:
            pass

    app.before_request(logger)


def bind_pyramid(config, get_user_id):
    import pyramid.events

    def logger(event):
        try:
            # TODO provide a proper API for this kind of stuff
            if event.request.path.startswith("/static"):
                return

            user_id = get_user_id(event)
            if user_id:
                log_request_info(
                    event.request.path, user_id, event.request.GET.dict_of_lists()
                )
        except Exception:
            pass

    config.add_subscriber(logger, pyramid.events.NewRequest)


def log_request_info(url, user_id, args):
    """Adds a log entry that fully represents the current request."""

    def flatten(dict_of_lists):
        return {
            key: value[0] if len(value) == 1 else value
            for key, value in dict_of_lists.items()
        }

    logging.info(
        "[FullRequestInfo] %s user=%s args=%s", url, user_id, json.dumps(flatten(args))
    )
