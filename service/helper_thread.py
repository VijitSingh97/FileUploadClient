import os

from client.upload_client import Client


class HelperThread:
    helper = "(Helper)"

    def __init__(self, delay=5, data_store="client_store/", verbose=True):
        self.delay = delay
        self.data_store = data_store
        self.verbose = verbose
        self.client = Client()

    def get_local_files(self):
        file_list = os.listdir(self.data_store)
        local_files = dict()
        for file in file_list:
            local_files[file] = os.path.getmtime(self.data_store + file)*1000
        return local_files

    def run_sync(self, local, remote):
        done = []
        # for our local files
        for f in local.keys():
            # if in remote
            if f in remote.keys():
                # if remote is newer by 500ms, download it
                if remote[f] - local[f] > 500:
                    if self.verbose:
                        print(f"{self.helper} downloading newer remote: {f} {remote[f]}. local {f} is {local[f]}")
                    self.client.download(f)
                # else if local is newer by 500ms, upload it
                elif local[f] - remote[f] > 500:
                    if self.verbose:
                        print(f"{self.helper} uploading newer local: {f}")
                    self.client.upload(f)
            # if not on remote server upload it
            else:
                if self.verbose:
                    print(f"{self.helper} uploading from local: {f}")
                self.client.upload(f)
            # mark f as done
            done.append(f)
        # in remote list, and not in done list, download it
        for f in remote:
            if f not in done:
                if self.verbose:
                    print(f"{self.helper} downloading from remote: {f}")
                self.client.download(f)

    # run every 5 secs
    def sync_task(self):
        if self.verbose:
            print(f"{self.helper} processing local file list")
        local = self.get_local_files()
        if self.verbose:
            print(f"{self.helper} downloading file list on remote")
        remote = self.client.get_files()
        self.run_sync(local, remote)
