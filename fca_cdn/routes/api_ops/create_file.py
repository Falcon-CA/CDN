import datetime
import os

from flask import Response, request

from cdn_global import cdn
from fca_cdn.util import create_id

CHUNK_SIZE = 512 * 1024


class OperationInfo:
    name = "create_file"
    form = ("FCA-Name", "FCA-Directory", "FCA-Private")
    files = ("FCA-File",)
    method = "POST"


@cdn.api_op(OperationInfo)
def operation(token, c):
    file = request.files["FCA-File"]
    name = request.form["FCA-Name"]
    directory = request.form["FCA-Directory"]
    private = request.form["FCA-Private"]

    response = _confirm_form(token, file, name, directory, private)
    if type(response) == Response:
        return response
    else:
        directory = response

    if private:
        if not token.create_file_p:
            return Response("No private file creation privileges", status=403)
    else:
        if not token.create_file:
            return Response("No file creation privileges", status=403)

    file_id, f_type, stamp = _create_info(file)
    cdn.file_index.add(file_id)

    upload_f = open(f"{cdn.file_path}/{file_id}", "ab")
    while True:
        try:
            chunk = file.stream.read(CHUNK_SIZE)
            if not chunk:
                break
            upload_f.write(chunk)
        except:
            upload_f.close()
            os.remove(f"{cdn.file_path}/{file_id}")
            cdn.file_index.remove(file_id)
            return Response("File failed to upload", status=500)

    c.execute("INSERT INTO files VALUES (%s, %s, %s, %s, %s, %s, %s)", (
        file_id,
        name,
        directory,
        f_type,
        os.stat(f"{cdn.file_path}/{file_id}").st_size,
        stamp,
        private
    ))
    cdn.db.commit()
    upload_f.close()
    return Response(file_id, status=201)


def _confirm_form(token, file, name, dir_, private):
    if token.max_file_size is not None:
        if file.content_length > token.max_file_size:
            return Response(
                "File size is bigger than your allowed upload size",
                status=413
            )

    if len(name) > 70:
        return Response("File name is too long", status=413)

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


def _create_info(file):
    file_id = create_id(10)
    while file_id in cdn.file_index or file_id in cdn.dir_index:
        file_id = create_id(10)

    f_split = file.filename.split(".")
    if len(f_split) == 1:
        f_type = None
    else:
        f_type = f_split[-1]

    stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    return file_id, f_type, stamp