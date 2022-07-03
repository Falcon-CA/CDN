import datetime

from flask import Response, request

from cdn_global import cdn
from fca_cdn.util import create_id


class OperationInfo:
    name = "create_directory"
    form = ("FCA-Name", "FCA-Directory", "FCA-Private")
    files = ()
    method = "POST"


@cdn.api_op(OperationInfo)
def operation(token, c):
    name = request.form["FCA-Name"]
    directory = request.form["FCA-Directory"]
    private = request.form["FCA-Private"]

    response = _confirm_form(name, directory, private)
    if type(response) == Response:
        return response
    else:
        directory = response

    if private:
        if not token.create_dir_p:
            return Response("No private directory creation privileges", status=403)
    else:
        if not token.create_dir:
            return Response("No directory creation privileges", status=403)

    dir_id, stamp = _create_info()
    cdn.dir_index.add(dir_id)
    c.execute("INSERT INTO directories VALUES (%s, %s, %s, %s, %s)", (
        dir_id,
        name,
        directory,
        stamp,
        private
    ))
    cdn.db.commit()

    return Response(dir_id, status=201)


def _confirm_form(name, dir_, private):
    if len(name) > 70:
        return Response("Directory name is too long", status=413)

    if dir_ == "":
        dir_ = None
    else:
        if dir_ not in cdn.dir_index:
            return Response("Given directory does not exist", status=404)

    try:
        private = int(private)
    except ValueError:
        return Response("Private argument must be 0 or 1", status=400)
    if private < 0 or private > 1:
        return Response("Private argument must be 0 or 1", status=400)

    return dir_


def _create_info():
    dir_id = create_id(10)
    while dir_id in cdn.file_index or dir_id in cdn.dir_index:
        dir_id = create_id(10)

    stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return dir_id, stamp