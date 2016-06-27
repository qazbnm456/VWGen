import os
import time
import shutil
import logging
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ModifiedHandler(FileSystemEventHandler):

    def __init__(self, fp):
        self.fp = fp

    def on_modified(self, event):
        self.fp.setLayers(self.fp.path)


class filePointer(object):
    """Class for reading and writing files."""

    pointer = ""
    path = None
    layers = None
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    def __init__(self, path=None, pointer="index.html"):
        self.event_handler = ModifiedHandler(self)
        self.observer = Observer()
        if path is not None:
            self.setLayers(path)
            self.observer.schedule(self.event_handler, path, recursive=True)
        self.pointer = pointer

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
    def write(fileName, content):
        """returns True if writing successfully, or False instead"""
        f = None
        try:
            f = open(fileName, 'w')
            f.write(content)
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
    def rmtree(path):
        """returns True if rmtree successfully, or False instead"""
        try:
            shutil.rmtree(path)
        except OSError, e:
            print(e)
            return False
        return True

    def zipExtract(self, fileName, dst):
        """returns True if zipExtract successfully, or False instead"""
        f = None
        try:
            f = zipfile.ZipFile(fileName, "r")
            f.extractall(dst)
            self.setLayers(dst)
            self.observer.schedule(self.event_handler, dst, recursive=True)
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

    def change(self, pointer="index.html"):
        self.pointer = pointer


if __name__ == "__main__":
    try:
        l = filePointer(path="../config/attacks/exec/", pointer="123")
        #ll = l.readLines("../config/attacks/execPayloads.txt")
        # for li in ll:
        #    print(li)
        # print l.layers
        l.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            l.observer.stop()
        l.observer.join()

    except SystemExit:
        pass
