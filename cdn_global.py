from flask import Flask


class CdnInstance(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_index = set()
        self.dir_index = set()
        self.token_index = set()
        self.db = None
        self.file_path = None
        self.api_ops = {}

    def api_op(self, info):
        def decor(func):
            info.func = func
            self.api_ops[info.name] = info
            return func
        return decor


cdn = CdnInstance(
    __name__,
    template_folder="fca_cdn/assets/html"
)