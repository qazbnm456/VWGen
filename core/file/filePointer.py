import os
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ModifiedHandler(FileSystemEventHandler):

    def __init__(self, fp):
        self.fp = fp

    def on_modified(self, event):
        self.fp.setLayers(self.fp.path)


class filePointer(object):
    """Class for manipulating files."""

    customizationPath = os.path.join(os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir)), "customization")
    tmpFile = None
    customizationClass = None

    pointer = None
    target = None
    path = None
    root = None
    layers = None

    def __init__(self, path=None, pointer="index.html", target="index.php"):
        self.event_handler = ModifiedHandler(self)
        self.observer = Observer()
        if path is not None:
            self.root = path[(path.rfind(os.sep) + 1):]
            self.setLayers(path)
            self.observer.schedule(
                self.event_handler, self.path, recursive=True)
        self.pointer = pointer
        self.target = target

    @staticmethod
    def readLines(fileName):
        """returns a array"""
        lines = []
        f = None
        try:
            # Reminder : don't try to read payload files as UTF-8, must give
            # str type
            f = open(fileName)
            for line in f:
                clean_line = line.strip(" \n")
                clean_line = clean_line.replace("[TAB]", "\t")
                clean_line = clean_line.replace("[LF]", "\n")
                if clean_line != "":
                    lines.append(clean_line.replace("\\0", "\0"))
        except IOError, e:
            print(e)
        finally:
            if f != None:
                f.close()
        return lines

    @staticmethod
    def read(fileName):
        """returns a src object"""
        src = None
        f = None
        try:
            f = open(fileName, 'rb')
            src = f.read()
        except IOError, e:
            print(e)
        finally:
            if f != None:
                f.close()
        return src

    @staticmethod
    def write(fileName, context, ext=".html"):
        """returns True if writing successfully, or False instead"""
        f = None
        try:
            if ext is not None:
                f = open(os.path.splitext(fileName)[0] + ext, 'wb')
            else:
                f = open(fileName, 'wb')
            f.write(context)
        except IOError, e:
            print(e)
            return False
        finally:
            if f != None:
                f.close()
        return True

    @staticmethod
    def copy(srcFile, dstFile):
        """returns True if copying successfully, or False instead"""
        try:
            shutil.copy(srcFile, dstFile)
        except IOError, e:
            print(e)
            return False
        return True

    @staticmethod
    def move(src, dst):
        try:
            shutil.move(src, dst)
        except (IOError, os.error), e:
            print(e)
            return False
        return True

    @staticmethod
    def rmtree(path):
        """returns True if rmtree successfully, or False instead"""
        try:
            shutil.rmtree(path)
        except OSError, e:
            print(e)
            return False
        return True

    def zipExtract(self, themePath, dst):
        """returns True if zipExtract successfully, or False instead"""
        f = None
        try:
            f = zipfile.ZipFile(themePath + '.zip', "r")
            f.extractall(dst)
            ind = themePath.rfind(os.sep) + 1
            self.root = themePath[ind:]
            self.setLayers(os.path.join(dst, self.root))
            self.observer.schedule(
                self.event_handler, self.path, recursive=True)
        except zipfile.BadZipfile, e:
            print(e)
            return False
        return True

    def dig(self, startpath):
        self.layers = {}
        rootdir = startpath.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, _, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = {file: os.path.splitext(file)[1] for file in files}
            parent = reduce(dict.get, folders[:-1], self.layers)
            parent[folders[-1]] = subdir

    def setLayers(self, path):
        if path is not None:
            self.path = path
            self.dig(self.path)

    def changePointer(self, pointer="index.html"):
        self.pointer = pointer
        return self.pointer

    def changeTarget(self, target="index.html"):
        self.target = target
        return self.target

    def findMainPointer(self):
        if self.root is not None:
            for ele in self.layers[self.root].values():
                if not isinstance(ele, dict):
                    if self.layers[self.root].keys()[self.layers[self.root].values().index(ele)] in ["index.htm", "index.html", "index.php", "main.html", "main.html", "main.php"]:
                        return self.changePointer(pointer=self.layers[self.root].keys()[self.layers[self.root].values().index(ele)])
            return self.changePointer()
        else:
            raise RuntimeError

    def cleanObserver(self):
        self.observer.unschedule_all()
        self.observer = Observer()

    def processInputFile(self, inputFile=None):
        if inputFile is not None:
            self.tmpFile = os.path.join(self.customizationPath, "instanceSample.py")
            self.copy(inputFile, self.tmpFile)

    def finishProcessInputFile(self):
        self.tmpFile = None
        self.customizationClass = None


if __name__ == "__main__":
    try:
        l = filePointer(path="../config/attacks", pointer="123")
        # ll = l.readLines("../config/attacks/execPayloads.txt")
        # for li in ll:
        #    print(li)
        # print l.layers
        l.findMainPointer()
        print l.pointer
        print l.target

    except SystemExit:
        pass
