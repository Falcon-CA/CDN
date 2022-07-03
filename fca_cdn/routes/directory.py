import json

from flask import Response, render_template, request

from cdn_global import cdn
from fca_cdn.obj.directory import Directory
from fca_cdn.obj.file import File
from fca_cdn.obj.token import Token


@cdn.route("/directory/<id_>", methods=["GET", "HEAD"])
def get_directory(id_):
    if id_ not in cdn.dir_index:
        return Response("Directory not found", status=404)

    c = cdn.db.cursor()
    directory = _get_dir_info(c, id_)
    if directory is None:
        return Response("Directory not found", status=404)

    if directory.private:
        private_response = _handle_private_dir(c)
        if type(private_response) == Response:
            return private_response

    mode = _determine_mode()
    if type(mode) == Response:
        return mode

    dirs, files = _get_dirs_and_files(c, id_)

    if request.method == "GET":
        if mode == "normal":
            response = Response(render_template(
                "folder.html",
                name=directory.name,
                len=len,
                round=round,
                directories=dirs,
                files=files,
                parent="/" if directory.dir is None else f"directory/{directory.dir}",
                self_dir=f"/directory/{directory.id}"
            ), status=200)
        elif mode == "csv":
            formatted_dirs = ",".join([dir_.id for dir_ in dirs])
            formatted_files = ",".join([file.id for file in files])
            response = Response(f"{formatted_dirs}\n{formatted_files}",
                                status=200, mimetype="text/csv")
        elif mode == "json":
            json_dict = {
                "directories": [dir_.id for dir_ in dirs],
                "files": [file.id for file in files]
            }
            response = Response(json.dumps(json_dict), status=200,
                                mimetype="text/json")
    else:
        response = Response(status=200)

    response.headers = {
        "FCA-ID": directory.id,
        "FCA-Name": directory.name,
        "FCA-Created": directory.created,
        "FCA-Private": directory.private,
        "FCA-Asset-Amount": len(dirs) + len(files)
    }
    return response


def _get_dir_info(c, id_):
    c.execute("SELECT * FROM directories WHERE id = %s", (id_,))
    dir_info = c.fetchone()

    if dir_info is None:
        return None
    else:
        return Directory.from_db(dir_info)


def _handle_private_dir(c):
    given_token = request.headers.get("FCA-Token")
    if given_token is None:
        return Response("No access token given", status=401)
    if given_token not in cdn.token_index:
        return Response("Given access token does not exist", status=401)

    c.execute("SELECT * FROM tokens WHERE id = %s", (given_token,))
    token_info = c.fetchone()
    if token_info is None:
        return Response("Given access token does not exist", status=401)

    token = Token.from_db(token_info)
    if not token.access_dir_p:
        return Response("No private directory access privileges", status=403)


def _determine_mode():
    mode = request.args.get("mode")
    if mode is None:
        return "normal"

    modes = ["normal", "json", "csv"]
    if mode in modes:
        return mode
    else:
        return Response("Invalid csv argument value", status=400)


def _get_dirs_and_files(c, id_):
    sorts = ["id", "name", "created", "size"]
    sort = request.args.get("sort")
    if sort is None:
        sort = "name"
    else:
        if sort not in sorts:
            return Response("Invalid sort", status=400)

    if sort == "size":
        c.execute("SELECT * FROM directories WHERE dir = %s AND private = 0 ORDER BY name", (id_,))
    else:
        c.execute(f"SELECT * FROM directories WHERE dir = %s AND private = 0 ORDER BY {sort}", (id_,))
    dirs = [Directory.from_db(dir_) for dir_ in c.fetchall()]

    c.execute(f"SELECT * FROM files WHERE dir = %s AND private = 0 ORDER BY {sort}", (id_,))
    files = [File.from_db(file) for file in c.fetchall()]

    return dirs, files