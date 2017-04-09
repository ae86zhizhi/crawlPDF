# -*- coding:utf-8 -*-

import libraries.pdf2txt
import os


def init():
    L = os.listdir('./docs/')
    L = [x for x in L if x.endswith('.pdf')]
    return L

def toXML(L):
    for item in L:
        cmd = "pdf2txt.py -o %s -t xml %s"%('./xmls/' + item[0: len(item) - 4] + '.xml', './docs/' + item)
        os.system(cmd)

def toTXT(L):
    for item in L:
        cmd = "pdf2txt.py -o %s -t text %s" % ('./texts/' + item[0: len(item) - 4] + '.txt', './docs/' + item)
        os.system(cmd)

def main():
    L = init()
    toXML(L)
    toTXT(L)