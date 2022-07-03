import os

from flask import Response, send_file

from cdn_global import cdn


@cdn.route("/asset/css/<file>")
def css_file(file):
    if file in os.listdir("fca_cdn/assets/css"):
        return send_file(f"fca_cdn/assets/css/{file}")
    else:
        return Response("CSS file not found", status=404)


@cdn.route("/asset/img/<file>")
def img_file(file):
    if file in os.listdir("fca_cdn/assets/img"):
        return send_file(f"fca_cdn/assets/img/{file}")
    else:
        return Response("Image file not found", status=404)