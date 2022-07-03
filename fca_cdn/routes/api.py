from flask import Response, request

from cdn_global import cdn
from fca_cdn.obj.token import Token


@cdn.route("/api", methods=["POST", "DELETE", "PUT"])
def api():
    operation = request.args.get("operation")
    if operation is None:
        return Response("No operation given in query string", status=400)
    if operation not in cdn.api_ops:
        return Response("Unknown API operation", status=404)

    op = cdn.api_ops[operation]
    response = _operation_params(op)
    if type(response) == Response:
        return response

    c = cdn.db.cursor()
    given_token = request.headers.get("FCA-Token")
    response = _confirm_token(given_token, c)
    if type(response) == Response:
        return response

    return op.func(Token.from_db(response), c)


def _operation_params(op):
    if request.method != op.method:
        return Response(f"This operation requires a {op.method} request",
                        status=405)
    for data in op.form:
        if data not in request.form:
            return Response(f"{data} not given in form", status=400)
    for file in op.files:
        if file not in request.files:
            return Response(f"{file} not given in files", status=400)


def _confirm_token(given, c):
    if given is None:
        return Response("No access token given", status=401)
    if given not in cdn.token_index:
        return Response("Given access token does not exist (E001)", status=401)

    c.execute("SELECT * FROM tokens WHERE token = %s", (given,))
    token_info = c.fetchone()
    if token_info is None:
        return Response("Given access token does not exist (E002)", status=401)

    return token_info