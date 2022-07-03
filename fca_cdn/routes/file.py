from flask import Response, redirect, request

from cdn_global import cdn
from fca_cdn.obj.file import File
from fca_cdn.obj.token import Token

CHUNK_SIZE = 512 * 1024


@cdn.route("/file/<id_>", methods=["GET", "HEAD"])
def get_file_by_id(id_):
    if id_ not in cdn.file_index:
        return Response("File not found", status=404)

    c = cdn.db.cursor()
    c.execute("SELECT name FROM files WHERE id = %s", (id_,))
    file_name = c.fetchone()

    if file_name is None:
        return Response("File not found", status=404)

    return redirect(f"/file/{id_}/{file_name[0]}")


@cdn.route("/file/<id_>/<name>", methods=["GET", "HEAD"])
def get_file(id_, name):
    if id_ not in cdn.file_index:
        return Response("File not found", status=404)

    c = cdn.db.cursor()
    file = _get_file_info(c, id_)
    if file is None:
        return Response("File not found", status=404)

    if file.private:
        private_response = _handle_private_file(c)
        if type(private_response) == Response:
            return private_response

    def file_buffer():
        with open(f"{cdn.file_path}/{id_}", "rb") as f:
            while True:
                try:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    else:
                        yield chunk
                except:
                    break

    if request.method == "GET":
        f_type = "text/plain" if file.type is None else file.type
        response = Response(file_buffer(), status=200, mimetype=f_type)
    else:
        response = Response(status=200)

    response.headers = {
        "FCA-ID": file.id,
        "FCA-Name": file.name,
        "FCA-Size": file.size,
        "FCA-Created": file.created,
        "FCA-Private": file.private
    }
    return response


def _get_file_info(c, id_):
    c.execute("SELECT * FROM files WHERE id = %s", (id_,))
    file_info = c.fetchone()

    if file_info is None:
        return None
    else:
        return File.from_db(file_info)


def _handle_private_file(c):
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
    if not token.access_file_p:
        return Response("No private file access privileges", status=403)