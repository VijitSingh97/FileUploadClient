import os

from client.upload_client import Client


class HelperThread:
    helper = "(Helper)"

    def __init__(self, delay=5, verbose=True):
        self.delay = delay
        self.verbose = verbose
        self.client = Client()

    def get_local_files(self):
        file_list = os.listdir(self.client.get_data_store())
        local_files = dict()
        for file in file_list:
            local_files[file] = os.path.getmtime(self.client.get_data_store() + file) * 1000
        return local_files

    def run_sync(self, local, remote):
        done = []
        printed = False
        # for our local files
        for f in local.keys():
            # if in remote
            if f in remote.keys():
                # if remote is newer by 500ms, download it
                if remote[f] - local[f] > 500:
                    if self.verbose:
                        print(f"\n{self.helper} downloading newer remote: {f} {remote[f]}. local {f} is {local[f]}",
                              end="")
                        printed = True
                    self.client.download(f)
                # else if local is newer by 500ms, upload it
                elif local[f] - remote[f] > 500:
                    if self.verbose:
                        print(f"\n{self.helper} uploading newer local: {f}", end="")
                        printed = True
                    self.client.upload(f)
            # if not on remote server upload it
            else:
                if self.verbose:
                    print(f"\n{self.helper} uploading from local: {f}", end="")
                    printed = True
                self.client.upload(f)
            # mark f as done
            done.append(f)
        # in remote list, and not in done list, download it
        for f in remote:
            if f not in done:
                if self.verbose:
                    print(f"\n{self.helper} downloading from remote: {f}", end="")
                    printed = True
                self.client.download(f)
        if printed:
            print("\n(Cmd) ", end="")

    # run every 5 secs
    def sync_task(self):
        local = self.get_local_files()
        remote = self.client.get_files()
        self.run_sync(local, remote)
