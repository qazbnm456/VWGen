import pycurl
import StringIO


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
        self.c.perform()
        r = self.b.getvalue()
        self.b.close()
        return r
