from werkzeug.exceptions import UnsupportedMediaType


class Request:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.bind_form()
        self.bind_args()
        self.bind_json()

    def bind_form(self):
        try:
            self.form = self.obj.form.to_dict()
        except Exception as e:
            self.form = {}
            pass

    def bind_args(self):
        try:
            self.args = self.obj.args
        except Exception as e:
            self.args = {}
            pass

    def bind_json(self):
        try:
            self.json = self.obj.json
        except Exception as e:
            self.json = {}
            pass

    def sort_response(self, data) -> None:
        data = {
            k: data[k]
            for k in sorted(data)
            if not k.lower().startswith("_")
        }
        files_value = data.pop("files")
        data["files"] = files_value
