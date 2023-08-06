# Standard lib imports
import os

class Logger():

    def __init__(self, outfile=None):
        self.outfile = self.create_file(outfile)
        self.enabled = True

    def write(self, msg):
        if not self.enabled:
            return

        if not isinstance(msg, str):
            msg = str(msg)

        with open(self.outfile, "at") as f:
            f.write(msg+"\n")

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def is_enabled(self):
        return self.enabled

    def create_file(self, filename):
        if filename is not None:
            return filename

        unique_extension = 0
        fname = "qwilfish_log.txt"
        while os.path.exists(fname):
            unique_extension += 1
            fname = "qwilfish_log_" + str(unique_extension) + ".txt"

        return fname

