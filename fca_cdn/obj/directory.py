class Directory:
    def __init__(self, **kw):
        self.id      = kw.get("id")
        self.name    = kw.get("name")
        self.dir     = kw.get("dir")
        self.created = kw.get("created")
        self.private = kw.get("private")

    @staticmethod
    def from_db(data):
        return Directory(
            id=data[0],
            name=data[1],
            dir=data[2],
            created=data[3],
            private=data[4]
        )