import json

from flask import Response, render_template, request

from cdn_global import cdn
from fca_cdn.obj.directory import Directory
from fca_cdn.obj.file import File


@cdn.route("/", methods=["GET", "HEAD"])
def home():
    c = cdn.db.cursor()
    mode = _determine_mode()
    if type(mode) == Response:
        return mode

    dirs, files = _get_dirs_and_files(c)

    if request.method == "GET":
        if mode == "normal":
            response = Response(render_template(
                "folder.html",
                name="Home",
                len=len,
                round=round,
                directories=dirs,
                files=files,
                parent=None,
                self_dir="/"
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
        "FCA-Asset-Amount": len(dirs) + len(files)
    }
    return response


def _determine_mode():
    mode = request.args.get("mode")
    if mode is None:
        return "normal"

    modes = ["normal", "json", "csv"]
    if mode in modes:
        return mode
    else:
        return Response("Invalid csv argument value", status=400)


def _get_dirs_and_files(c):
    sorts = ["id", "name", "created", "size"]
    sort = request.args.get("sort")
    if sort is None:
        sort = "name"
    else:
        if sort not in sorts:
            return Response("Invalid sort", status=400)

    if sort == "size":
        c.execute("SELECT * FROM directories WHERE dir IS NULL AND private = 0 ORDER BY name")
    else:
        c.execute(f"SELECT * FROM directories WHERE dir IS NULL AND private = 0 ORDER BY {sort}")
    dirs = [Directory.from_db(dir_) for dir_ in c.fetchall()]

    c.execute(f"SELECT * FROM files WHERE dir IS NULL AND private = 0 ORDER BY {sort}")
    files = [File.from_db(file) for file in c.fetchall()]

    return dirs, files