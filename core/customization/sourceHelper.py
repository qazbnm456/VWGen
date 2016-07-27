import pycurl
import StringIO
from ..file.logger import Logger


class sourceHelper(object):

    def __init__(self):
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.TIMEOUT, 5)
        self.c.setopt(pycurl.FOLLOWLOCATION, True)

    def setUrl(self, url):
        self.b = StringIO.StringIO()
        self.c.setopt(pycurl.WRITEFUNCTION, self.b.write)

        self.c.setopt(pycurl.URL, url)

    def perform(self):
        try:
            self.c.perform()
        except pycurl.error as e:
            Logger.logError("\n" + "[ERROR] " + e[1])
            Logger.logInfo(
                "\n[INFO] Taking you to safely leave the program.")
            raise RuntimeError
        r = self.b.getvalue()
        self.b.close()
        return r
