# -*- coding:utf-8 -*-

import downloadPDF
import translateToXML
import insertToDB

def start():
    downloadPDF.main()
    translateToXML.main()
    insertToDB.main()

start()