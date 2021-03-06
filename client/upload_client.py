import ast
import os
from pathlib import Path

import requests


class Client:
    def __init__(self, url="http://localhost:8080", data_store="client_store/"):
        self.url = url
        self.data_store = data_store

    def get_data_store(self):
        p = Path(self.data_store)
        if not p.exists():
            os.mkdir(self.data_store)
        return self.data_store

    def upload(self, inp):
        # open file
        with open(self.get_data_store() + inp, 'rb') as f:
            # upload and return response
            r = requests.post(self.url + "/upload", files={'file': f})
            # touch local for timestamps
            Path(self.get_data_store() + inp).touch()
            return r.text

    def download(self, name):
        r = requests.get(self.url + "/download?name=" + name)
        if r.status_code == 200:
            open(self.get_data_store() + name, 'wb').write(r.content)
            return f"downloaded {name}"
        else:
            return f"failed to download {name}"

    def delete(self, name):
        os.remove(self.get_data_store() + name)
        return requests.delete(self.url + "/delete", data=name).text

    def rename(self, args):
        # check args len
        if len(args) != 2:
            raise Exception(f"bad args: {args}")
        # rename locally
        os.rename(self.get_data_store() + args[0], self.get_data_store() + args[1])
        # rename remote server
        req = {
            "oldName": args[0],
            "newName": args[1]
        }
        return requests.put(self.url + "/rename", json=req).text

    def get_files(self):
        local = dict()
        response_text = requests.get(self.url + "/getFiles").text
        if response_text:
            for file in ast.literal_eval(response_text):
                local[file['name']] = file['lastModified']
        return local
