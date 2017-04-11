# -*- coding:utf-8 -*-

import mysql.connector
import os
from libraries import stringlib
from extarctXML import extractTitle

class mysqlManipulator:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS homework;")
        self.cursor.execute("USE homework;")
        self.cursor.execute("DROP TABLE IF EXISTS usdaplant;")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usdaplant(`symbol` VARCHAR(12) PRIMARY KEY, `scientific_name` VARCHAR(40), `common_name` VARCHAR(40)) ENGINE=MyISAM;")
        self.lf = open('./log.txt','w')

    def __delete__(self):
        self.cursor.close()

    #list position of labels in the text
    def findLabelPos(self, content, labels):
        labelpos = [0]
        for lb in labels:
            labelpos.append(content.find(lb, labelpos[-1]))
        return labelpos[1:]


    def handleBasic(self, basicInfo):
        basicInfo = basicInfo.replace('\'', '\\\'')
        infos = basicInfo.split(',')
        sql = 'INSERT INTO usdaplant(`symbol`, `scientific_name`, `common_name`) VALUES('
        for info in infos:
            sql += '\'' + info + '\'' + ','
        sql = sql[:-1] + ');'
        self.lf.write(sql + '\n')
        self.lf.flush()
        self.cursor.execute(sql)
        self.connection.commit()

    def handlePDF(self, line):  #handle rows in PDF from basic information
        sym = line[0: line.find(',')]
        fs = './docs/fs_' + sym + '.pdf'
        pg = './docs/pg_' + sym + '.pdf'
        if os.path.exists(fs):
            self.__handleOthers('./xmls/fs_' + sym + '.xml', './texts/fs_' + sym + '.txt', line)
        if os.path.exists(pg):
            self.__handleOthers('./xmls/pg_' + sym + '.xml', './texts/pg_' + sym + '.txt', line)

    def handleUpdateData(self, line, labels):
        row = line.split(',')  #obtain the tuple
        row = [stringlib.text_to_sql(ele) for ele in row]
        labels = [stringlib.textToIdentifier(ele.strip().strip(':')) for ele in labels]
        sql = 'UPDATE usdaplant SET '
        l = len(labels)
        lrow = len(row)
        if l != lrow:
            return
        for i in range(0, l):
            sql += "%s=%s,"%('`' + labels[i] + '`', '\'' + row[i] + '\'')
        sql = sql[:-1] + ' WHERE symbol = ' + '\'' + row[0] + '\'' + ';'
        self.lf.write(sql + '\n')
        self.lf.flush()
        self.cursor.execute(sql)
        self.connection.commit()


    def __handleOthers(self, fileXML, fileTXT, basicInfo):  #including table and data
        fpt = open(fileTXT, 'r')
        labels = extractTitle(fileXML)
        content = fpt.read()
        self.handleTable(labels)
        self.__handleOtherData(labels, content, basicInfo, fileTXT.find('fs_') != -1)
        fpt.close()

    def handleTable(self, labels):
        for lb in labels:
            try:
                sql = "ALTER TABLE usdaplant ADD COLUMN %s TEXT;"%('`' + stringlib.textToIdentifier(lb) + '`')
                self.cursor.execute(sql)
                self.connection.commit()
            except Exception as e:
                pass                 #duplicate column, neglect

    def __handleOtherData(self, labels, contentPDF, basicInfo, is_fs = True):
        labelpos = self.findLabelPos(contentPDF, labels)
        labelpos.append(len(contentPDF))
        prefix = 'fs_' if is_fs else 'pg_'
        labels = [stringlib.textToIdentifier(prefix + lb) for lb in labels]
        sql = "UPDATE usdaplant SET "
        for i in range(0, len(labels)):
            sql += "%s=%s,"%('`' + labels[i] + '`', '\'' + stringlib.text_to_sql(contentPDF[labelpos[i] + len(labels[i]) - 1: labelpos[i + 1]]) + '\'')
        sql = sql[:-1] + "WHERE symbol='" + basicInfo[0: basicInfo.find(',')] + "';"
        self.lf.write(sql + '\n')
        self.lf.flush()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            pass

def main():
    mm = mysqlManipulator(mysql.connector.connect(user='root', password="?&*()NSDWE19", database='homework', use_unicode=True))
    fp = open('./basics/basicInfo.txt', 'r')   #pdfs and basic
    while True:
        line = fp.readline().strip()
        if not line:
            break
        mm.handleBasic(line)
        mm.handlePDF(line)
    fp.close()

    fp = open('./basics/profile.csv','r')
    labels = fp.readline().strip().split(',')
    mm.handleTable(labels)
    while True:
        line = fp.readline().strip()
        if not line:
            break
        mm.handleUpdateData(line, labels)
    fp.close()

    fp = open('./basics/character.csv', 'r')
    labels = fp.readline().strip().split(',')
    mm.handleTable(labels)
    while True:
        line = fp.readline().strip()
        if not line:
            break
        mm.handleUpdateData(line, labels)
    fp.close()



