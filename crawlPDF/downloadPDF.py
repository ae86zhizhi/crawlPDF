# -*- coding:utf-8 -*-

from selenium import webdriver
import urllib
import urllib2
import os
import re
import codecs
import extractProfile
import extractCharacter

def extract(source):
    pstart = source.find('Fact Sheets and Plant Guides',0)
    pattern = '<tr class=\"rowon\">'
    pattern2end = '</th>'
    pend = source.find('</tbody>',source.find(pattern))
    p = pstart - 1
    Lret = []
    LSym = []
    LCmn = []
    Labbr = []
    while p < pend:
        p = source.find(pattern, p + 1)
        if p == -1:
            break
        p2end = source.find(pattern2end, p)
        p2start = source.find('>', p + len(pattern))
        if p2end <= p2start:
            continue
        psym1 = source.find('<em>', p2end)
        psym2 = source.find('<em>', psym1 + 1)
        pCmn = source.find('<td>', psym2)
        LSym.append(source[psym1 + len('<em>'): source.find('</em>', psym1)] + ' ' + source[psym2 + len('<em>'): source.find('</em>', psym2)])
        LCmn.append(source[pCmn + len('<td>'): source.find('</td>', pCmn)])
        Labbr.append(source[p2start + 1: p2end])
        Lret.append('https://plants.usda.gov/factsheet/pdf/fs_' + source[p2start + 1: p2end] + '.pdf')
        Lret.append('https://plants.usda.gov/plantguide/pdf/pg_' + source[p2start + 1: p2end] + '.pdf')
    return Lret, LSym, LCmn, Labbr

def downloadByURL(list):
    for file in list:
        try:
            p1 = file.find('fs_')
            p2 = file.find('pg_')
            p = p2 if p1 == -1 else p1
            urllib.urlretrieve(file, './docs/' + file[p:])
            print(file[p:] + 'downloaded' + '\r\n')
        except Exception as e:
            print(e.message)

def deleteSomething():
    pdfs = os.listdir('./docs')
    pdfs = [x for x in pdfs if x.endswith('.pdf')]
    need_to_del = [x for x in pdfs if os.path.getsize('./docs/' + x) <= 34 * 1024]
    for item in need_to_del:
        os.remove('./docs/' + item)

def writeToFileBasic(Labbr, Lsym, Lcmn):
    fp = open('./basics/basicInfo.txt','w')
    l = len(Lsym)
    for i in range(0, l):
        fp.write(Labbr[i] + ',' + Lsym[i] + ',' + Lcmn[i] + '\n')
    fp.flush()
    fp.close()

def writeToFileProfile(Labbr):
    fp = open('./basics/profile.csv','w')  #truncate
    fp.close()
    extractProfile.writeProfileLabelToFile()
    for lb in Labbr:
        try:
            addr = 'https://plants.usda.gov/core/profile?symbol=' + lb
            content = urllib.urlopen(addr).read()
            extractProfile.getProfile(content)
        except Exception as e:
            print('profile_label ' + lb + ': ' + e.message)

def writeToFileCharacteristics(Labbr):
    fp = open('./basics/character.csv', 'w')
    fp.close()
    l = len(Labbr)
    for i in range(0, l):
        try:
            addr = 'https://plants.usda.gov/java/charProfile?symbol=' + Labbr[i]
            content = urllib.urlopen(addr).read()
            if i == 0:
                extractCharacter.writeColumnNamesToFile(content)
            extractCharacter.writeCharacteristicToFile(Labbr[i],extractCharacter.getColumnNames(content), content)
        except Exception as e:
            print('character_label ' + Labbr[i] + ': ' + e.message)


def main():
    request = webdriver.Chrome('/Users/apple/ChromeApp/chromedriver')
    request.get('https://plants.usda.gov/java/factSheet')
    str = request.page_source.encode('utf-8')

    Lret, Lsym, Lcmn, Labbr = extract(str)
    writeToFileBasic(Labbr, Lsym, Lcmn)
    writeToFileProfile(Labbr)
    writeToFileCharacteristics(Labbr)
    downloadByURL(Lret)
    deleteSomething()

main()

q


