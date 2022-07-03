class File:
    def __init__(self, **kw):
        self.id      = kw.get("id")
        self.name    = kw.get("name")
        self.dir     = kw.get("dir")
        self.type    = kw.get("type")
        self.size    = kw.get("size")
        self.created = kw.get("created")
        self.private = kw.get("private")

    @staticmethod
    def from_db(data):
        return File(
            id=data[0],
            name=data[1],
            dir=data[2],
            type=data[3],
            size=data[4],
            created=data[5],
            private=data[6]
        )