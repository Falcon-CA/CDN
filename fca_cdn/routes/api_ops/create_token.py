import datetime
import json

from flask import Response, request

from cdn_global import cdn
from fca_cdn.util import create_id

_perms = (
    "access_file_p", "access_dir_p",
    "create_file", "create_file_p",
    "create_dir", "create_dir_p",
    "delete_file", "delete_dir"
)


class OperationInfo:
    name = "create_token"
    form = ("FCA-Perms", "FCA-Expiration", "FCA-Upload-Max")
    files = ()
    method = "POST"


@cdn.api_op(OperationInfo)
def operation(token, c):
    if not token.admin:
        return Response("No administrator privileges", status=403)

    perms = request.form["FCA-Perms"]
    exp = request.form["FCA-Expiration"]
    upload = request.form["FCA-Upload-Max"]

    response = _confirm_form(perms, exp, upload)
    if type(response) == Response:
        return response
    else:
        perms = response[0]
        exp = response[1]
        upload = response[2]

    token_id, stamp = _create_info()
    cdn.token_index.add(token_id)
    c.execute("INSERT INTO tokens VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
        token_id,
        stamp,
        exp,
        "access_file_p" in perms,
        "access_dir_p" in perms,
        "create_file" in perms,
        "create_file_p" in perms,
        "create_dir" in perms,
        "create_dir_p" in perms,
        "delete_file" in perms,
        "delete_dir" in perms,
        False,
        upload
    ))
    cdn.db.commit()

    return Response(token_id, status=201)


def _confirm_form(perms, exp, upload):
    try:
        perms = json.loads(perms)
    except json.JSONDecodeError:
        return Response("Invalid permission JSON string", status=400)
    for perm in perms:
        if perm not in _perms:
            return Response(f"{perm} is not a valid permissions", status=400)

    try:
        exp = int(exp)
    except ValueError:
        return Response("Expiration must be an integer", status=400)
    if exp == 0:
        exp = None
    else:
        if exp < 0:
            return Response("Expiration must be greater than 0", status=400)

    try:
        upload = int(upload)
    except ValueError:
        return Response("Upload max must be an integer", status=400)
    if upload == 0:
        upload = None
    else:
        if exp < 0:
            return Response("Upload max must be greater than 0", status=400)

    return (perms, exp, upload)


def _create_info():
    token_id = create_id(45)
    while token_id in cdn.token_index:
        token_id = create_id(45)

    stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return token_id, stamp