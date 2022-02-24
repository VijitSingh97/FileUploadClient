from cmd import Cmd

from client.upload_client import Client


class Prompt(Cmd):
    client = Client()

    @staticmethod
    def do_exit(inp):
        """exit the client."""
        print("Thanks!")
        return True

    def do_upload(self, inp):
        """upload file to server. ex: upload data/data.txt"""
        try:
            print(inp)
            print(self.client.upload(inp))
        except Exception as e:
            print(f"{e}")

    def do_rename(self, inp):
        """rename the file on the local and remote server"""
        try:
            print(self.client.rename(str.split(inp, " ")))
        except Exception as e:
            print(f"{e}")

    def do_delete(self, inp):
        """delete the file on local and remote server"""
        try:
            print(self.client.delete(inp))
        except Exception as e:
            print(f"{e}")

    def do_download(self, inp):
        """download file from remote server"""
        print(self.client.download(inp))

    def do_get_files(self, inp):
        """get files on remote server"""
        print(self.client.get_files())
