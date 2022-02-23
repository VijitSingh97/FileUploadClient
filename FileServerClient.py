from cmd import Cmd
import requests

class FileServerClient(Cmd):
    upload_url = "http://localhost:8080/upload"
    def do_exit(self, inp):
        '''exit the client.'''
        print("Thanks!")
        return True
    def do_upload(self, inp):
        '''upload file to server. ex: upload data/data.txt'''
        with open(inp, 'rb') as f:
            r = requests.post(self.upload_url, files={inp: f})
            print(r.text)
    def do_rename(self, inp):
        # rename on local and remote
        pass
    def do_delete(self, inp):
        # delete on local and remote
        pass
    def do_download(self,inp):
        pass