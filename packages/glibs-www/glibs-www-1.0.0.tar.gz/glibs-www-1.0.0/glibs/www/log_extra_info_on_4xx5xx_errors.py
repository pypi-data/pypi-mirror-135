import json
import logging

__all__ = ["bind_pyramid", "bind_flask"]

logger = logging.getLogger(__name__)


def bind_pyramid(config, log_maxsize=5000):
    import pyramid.events

    def log(logline):
        if len(logline) > log_maxsize:
            logline = logline[:log_maxsize] + "\n(...) [full body not shown]"
        logger.info(logline)

    def keep_a_copy_of_400_error_messages(event):
        if event.response.status_code >= 400:
            try:
                log("Request\n{}".format(json.dumps(event.request.json_body, indent=4)))
            except Exception:
                pass

        if 400 <= event.response.status_code < 500:
            try:
                log(
                    "Response\n{}".format(
                        json.dumps(event.response.json_body, indent=4)
                    )
                )
            except Exception:
                pass

    config.add_subscriber(keep_a_copy_of_400_error_messages, pyramid.events.NewResponse)


def bind_flask(app, log_maxsize):
    import flask

    def log(logline):
        if len(logline) > log_maxsize:
            logline = logline[:log_maxsize] + "\n(...) [full body not shown]"
        logger.info(logline)

    def keep_a_copy_of_400_error_messages(response):
        if response.status_code >= 400:
            try:
                log("Request\n{}".format(json.dumps(flask.request.json, indent=4)))
            except Exception:  # pragma: no cover
                pass

        if 400 <= response.status_code < 500:
            try:
                log(
                    "Response\n{}".format(
                        json.dumps(json.loads(response.data), indent=4)
                    )
                )
            except Exception:
                pass

        return response

    app.after_request(keep_a_copy_of_400_error_messages)
