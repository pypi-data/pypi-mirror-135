import datetime
import os
import socket


class Status:
    def __init__(self, dir_):
        self.dir = dir_
        self.status = "status"
        for status in ["Done", "Failed", "Running"]:
            if os.path.exists(os.path.join(dir_, status)):
                self.status = status

        self.status_path = os.path.join(dir_, self.status)

    def done(self):
        self._set_status("Done")

    def running(self):
        self._set_status("Running")

    def failed(self):
        self._set_status("Failed")

    def _set_status(self, status):
        timestamp = datetime.datetime.now().strftime("%y/%m/%d-%H:%M:%S")

        if not os.path.exists(self.status_path):
            with open(self.status_path, "w") as f:
                f.write("Host: " + socket.gethostname() + "\n")

        with open(self.status_path, "a") as status_file:
            status_file.write(status + ": " + timestamp + "\n")

        status_path = os.path.join(self.dir, status)
        os.rename(self.status_path, status_path)

        self.status = status
        self.status_path = status_path
