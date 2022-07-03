import os

from flask import Response, request

from cdn_global import cdn

CHUNK_SIZE = 512 * 1024


class OperationInfo:
    name = "edit_file"
    form = ("FCA-FileID", "FCA-Name")
    files = ("FCA-File",)
    method = "PUT"


@cdn.api_op(OperationInfo)
def operation(token, c):
    file_name = request.form["FCA-Name"]
    file_id = request.form["FCA-FileID"]
    file = request.files["FCA-File"]

    if not token.create_file:
        return Response("No file creation privileges (For edit)", status=403)

    c.execute("UPDATE files SET name = %s WHERE id = %s", (
        file_name,
        file_id
    ))

    edit_f = open(f"{cdn.file_path}/{file_id}", "wb")
    while True:
        try:
            chunk = file.stream.read(CHUNK_SIZE)
            if not chunk:
                break
            edit_f.write(chunk)
        except:
            edit_f.close()
            return Response("File failed to upload", status=500)

    cdn.db.commit()
    edit_f.close()
    return Response("File edited", status=200)