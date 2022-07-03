from flask import Response, request

from cdn_global import cdn
from fca_cdn.init import get_connection
from fca_cdn.util import log

USER_IP_H = "CF-Connecting-IP"


@cdn.before_request
def before_request():
    if not cdn.db.is_connected():
        log("Database connection was closed and has been reopened")
        cdn.db = get_connection()

    user_ip = request.headers.get(USER_IP_H)
    if user_ip is None:
        log(f"{request.remote_addr} - {request.method} {request.path}", level="request")
    else:
        log(f"{user_ip} - {request.method} {request.path}", level="request")


@cdn.errorhandler(404)
def handle_404(e):
    return Response("Request path not found", status=404)


@cdn.errorhandler(405)
def handle_405(e):
    return Response("Request method not allowed", status=405)


@cdn.errorhandler(500)
def handle_500(e):
    return Response("An unexpected error has occurred "
                    "and your request could not be "
                    "completed", status=500)