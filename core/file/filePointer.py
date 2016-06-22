import os
import sys

class filePointer(object):
    """Class for reading and writing files"""
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


if __name__ == "__main__":
    try:
        l = filePointer()
        ll = l.readLines("../config/attacks/execPayloads.txt")
        for li in ll:
            print(li)
    except SystemExit:
        pass
