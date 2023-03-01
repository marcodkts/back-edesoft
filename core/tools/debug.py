from asbool import asbool
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from stela import settings


def show_toolbar(request: WSGIRequest) -> bool:
    """Show Django Debug Toolbar.

    Original code: debug_toolbar.middleware.show_toolbar

    :param request: WSGIRequest
    :return: boolean
    """

    return asbool(settings["project.show_debug_toolbar"]) and settings["project.debug"]
