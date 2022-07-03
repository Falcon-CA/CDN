class Token:
    def __init__(self, **kw):
        self.token         = kw.get("token")
        self.issued_at     = kw.get("issued_at")
        self.exp_sec       = kw.get("exp_sec")
        self.access_file_p = kw.get("access_file_p")
        self.access_dir_p  = kw.get("access_dir_p")
        self.create_file   = kw.get("create_file")
        self.create_file_p = kw.get("create_file_p")
        self.create_dir    = kw.get("create_dir")
        self.create_dir_p  = kw.get("create_dir_p")
        self.delete_file   = kw.get("delete_file")
        self.delete_dir    = kw.get("delete_dir")
        self.admin         = kw.get("admin")
        self.max_file_size = kw.get("max_size_size")

    @staticmethod
    def from_db(data):
        return Token(
            token=data[0],
            issued_at=data[1],
            exp_sex=data[2],
            access_file_p=data[3],
            access_dir_p=data[4],
            create_file=data[5],
            create_file_p=data[6],
            create_dir=data[7],
            create_dir_p=data[8],
            delete_file=data[9],
            delete_dir=data[10],
            admin=data[11],
            max_file_size=data[12]
        )