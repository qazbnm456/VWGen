import os
import sys
import shutil
import zipfile

class filePointer(object):
    """Class for reading and writing files"""

    pointer = ""

    def __init__(self, pointer="index.html"):
        self.pointer = pointer


    @staticmethod
    def readLines(fileName):
        """returns a array"""
        lines = []
        f = None
        try:
            # Reminder : don't try to read payload files as UTF-8, must give str type
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


    @staticmethod
    def zipExtract(fileName, dst):
        """returns True if zipExtract successfully, or False instead"""
        f = None
        try:
            f = zipfile.ZipFile(fileName, "r")
            f.extractall(dst)
        except BadZipfile, e:
            print(e)
            return False
        return True


    def change(self, pointer="index.html"):
        self.pointer = pointer


if __name__ == "__main__":
    try:
        l = filePointer(pointer="123")
        #ll = l.readLines("../config/attacks/execPayloads.txt")
        #for li in ll:
        #    print(li)
        l.change()
        print l.pointer
    except SystemExit:
        pass
