from flask import Response, request

from cdn_global import cdn


class OperationInfo:
    name = "delete_directory"
    form = ("FCA-Directory",)
    files = ()
    method = "DELETE"


@cdn.api_op(OperationInfo)
def operation(token, c):
    if not token.delete_dir:
        return Response("No directory deletion privileges", status=403)

    directory = request.form["FCA-Directory"]
    if directory not in cdn.dir_index:
        return Response("Directory not found", status=404)

    cdn.dir_index.remove(directory)
    c.execute("DELETE FROM directories WHERE id = %s", (directory,))
    cdn.db.commit()

    return Response("Directory deleted", status=200)