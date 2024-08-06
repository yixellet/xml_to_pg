import os
from zipfile import ZipFile, is_zipfile

from parser import Parser

def recursion(cur, conn, dirPath, schema):
    content = os.listdir(dirPath)
    for item in content:
        path = os.path.join(dirPath, item)
        if os.path.isfile(path):
            if os.path.splitext(item)[1] == '.xml':
                with open(path, encoding="utf8") as f:
                    p = Parser(f)
                    if p.getFileType():
                        p.parse(cur, conn, schema)

        if is_zipfile(path):
            with ZipFile(path, "r") as zip:
                for f in zip.infolist():
                    if f.filename.split('.')[-1] == 'xml':
                        with zip.open(f.filename, 'r') as xml_from_zip:
                            p = Parser(xml_from_zip)
                            if p.getFileType():
                                p.parse(cur, conn, schema)
        if os.path.isdir(path):
            recursion(path)