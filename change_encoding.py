#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
import re
import codecs
import chardet

def convert(filename, target_encoding="UTF-8"):
    try:
        content = codecs.open(filename, 'r').read()
        source_encoding = chardet.detect(content)['encoding']

        if content is not '' and source_encoding is not None:
            content = content.decode(source_encoding)
            codecs.open(filename, 'w', encoding=target_encoding).write(content)
            newcontent = codecs.open(filename, 'r').read()
            new_encoding = chardet.detect(newcontent)['encoding']
            print (new_encoding)

    except IOError as err:
        print("I/O error:{0}".format(err))


def explore(dir):
    for root, dirs, files in os.walk(dir):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            if re.match('.cpp|.h',os.path.splitext(file)[1]):
                print(file)
                path = os.path.join(root, file)
                convert(path)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        arg1 = sys.argv[1]
        print (arg1)
        if os.path.isfile(arg1):
            convert(arg1)
        elif os.path.exists(arg1):
             explore(arg1)
    print ("finished!")