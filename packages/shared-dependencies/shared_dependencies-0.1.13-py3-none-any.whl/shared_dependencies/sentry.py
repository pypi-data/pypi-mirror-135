import os
import logging
from sentry_sdk import capture_exception, init
from sentry_sdk.integrations.pure_eval import PureEvalIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = logging.getLogger("uvicorn")

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

common_integrations = [
    sentry_logging,
    PureEvalIntegration(),
]


def init_sentry(sentry_integrations: common_integrations):
    """
    This method has to be called in the app init file (main.py).
    SENTRY_DSN, SENTRY_ENVIRONMENT and SENTRY_RELEASE must be provided in app variables.
    :param sentry_integrations:
    :return: sentry init function
    """
    return init(
        integrations=sentry_integrations,
        traces_sample_rate=float(os.getenv("TRACES_SAMPLE_RATE_SENTRY", 1.0)),
        sample_rate=float(os.getenv("SAMPLE_RATE_SENTRY", 1.0)),
        traces_sampler=sampling_context,
    )


def sampling_context(context):
    try:
        if "/metrics" in context["asgi_scope"].get("path", ""):
            return 0
    except KeyError:
        logger.exception("context->asgi_scope failed")
        return 0
    else:
        logger.info(f'sentry-trace : {context["transaction_context"]["trace_id"]}')
        return float(os.getenv("TRACES_SAMPLE_RATE_SENTRY", 1.0))