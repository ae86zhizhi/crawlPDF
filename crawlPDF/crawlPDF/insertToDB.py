# -*- coding:utf-8 -*-

import mysql.connector
import os
from extarctXML import extractTitle

class mysqlManipulator:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS homework;")
        self.cursor.execute("USE homework;")
        self.cursor.execute("DROP TABLE IF EXISTS usdaplant;")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usdaplant(symbol VARCHAR(12) PRIMARY KEY, scientific_name VARCHAR(40), common_name VARCHAR(40));")

    def __delete__(self):
        self.cursor.close()

    #list position of labels in the text
    def findLabelPos(self, content, labels):
        labelpos = [0]
        for lb in labels:
            labelpos.append(content.find(lb, labelpos[-1]))
        return labelpos[1:]

    def handleTable(self, labels, is_fs = True):
        prefix = "fs_" if is_fs else "pg_"
        for lb in labels:
            try:
                sql = "ALTER TABLE usdaplant ADD COLUMN %s TEXT;"%(prefix + self.textToIdentifier(lb))
                self.cursor.execute(sql)
                self.connection.commit()
            except Exception as e:
                pass                 #duplicate column, neglect

    def textTosqlText(self, s):
        return s.replace("\\", "\\\\").replace("'", "\\'")

    def textToIdentifier(self, s):
        x = ''
        for i in range(0, len(s)):
            if not ('A' <= s[i] <= 'Z') and not ('a' <= s[i] <= 'z') and not ('0' <= s[i] <= '9') and s[i] != '_':
                x += '_'
            else:
                x += s[i]
        return x

    def handleBasic(self, basicInfo):
        basicInfo = basicInfo.replace('\'', '\\\'')
        infos = basicInfo.split(',')
        sql = 'INSERT INTO usdaplant(symbol, scientific_name, common_name) VALUES('
        for info in infos:
            sql += '\'' + info + '\'' + ','
        sql = sql[:-1] + ');'
        self.cursor.execute(sql)
        self.connection.commit()

    def handleOtherData(self, labels, contentPDF, basicInfo, is_fs = True):
        prefix = "fs_" if is_fs else "pg_"
        labelpos = self.findLabelPos(contentPDF, labels)
        labelpos.append(len(contentPDF))
        labels = [self.textToIdentifier(prefix + lb) for lb in labels]
        sql = "UPDATE usdaplant SET "
        for i in range(0, len(labels)):
            sql += "%s=%s,"%(labels[i], '\'' + self.textTosqlText(contentPDF[labelpos[i] + len(labels[i]) - 1: labelpos[i + 1]]) + '\'')
        sql = sql[:-1] + "WHERE symbol='" + basicInfo[0: basicInfo.find(',')] + "';"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            pass


    def handleOthers(self, fileXML, fileTXT, basicInfo):
        fpt = open(fileTXT, 'r')
        labels = extractTitle(fileXML)
        content = fpt.read()
        self.handleTable(labels, fileTXT.startswith('fs_'))
        self.handleOtherData(labels, content, basicInfo, fileTXT.startswith('fs_'))
        fpt.close()

def main():
    mm = mysqlManipulator(mysql.connector.connect(user='root', password="******", database='homework', use_unicode=True))
    fp = open('./basics/basicInfo.txt', 'r')
    while True:
        line = fp.readline()[:-1]
        if not line:
            break
        mm.handleBasic(line)
        sym = line[0: line.find(',')]
        fs = './docs/fs_' + sym + '.pdf'
        pg = './docs/pg_' + sym + '.pdf'
        if os.path.exists(fs):
           mm.handleOthers('./xmls/fs_' + sym + '.xml', './texts/fs_' + sym + '.txt', line)
        if os.path.exists(pg):
           mm.handleOthers('./xmls/pg_' + sym + '.xml', './texts/pg_' + sym + '.txt', line)
    fp.close()
