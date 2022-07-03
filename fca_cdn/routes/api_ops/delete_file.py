import os

from flask import Response, request

from cdn_global import cdn


class OperationInfo:
    name = "delete_file"
    form = ("FCA-File",)
    files = ()
    method = "DELETE"


@cdn.api_op(OperationInfo)
def operation(token, c):
    if not token.delete_file:
        return Response("No file deletion privileges", status=403)

    file = request.form["FCA-File"]
    if file not in cdn.file_index:
        return Response("File not found", status=404)

    cdn.dir_index.remove(file)
    os.remove(f"{cdn.file_path}/{file}")
    c.execute("DELETE FROM files WHERE id = %s", (file,))
    cdn.db.commit()

    return Response("File deleted", status=200)