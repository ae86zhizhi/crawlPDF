import re
import os
import codecs


#characteristic_pattern1 = re.compile(r'<tr>........<td valign="top" align="left">(.+?)</td>........<td valign="top" align="left">(.+?)</td>......</tr>',re.S)



def getColumnNames(content):
    characteristic_pattern = re.compile(r'<tr>........<td valign="top" align="left">(.+?)</td>.+?</tr>', re.S)
    col_name = characteristic_pattern.findall(content)
    return col_name

def writeColumnNamesToFile(content):
    output = open('./basics/character.csv', 'a')
    columnNames = getColumnNames(content)
    str = ''
    for name in columnNames:
        str += name.replace(',', '_') + ','
    output.write(str.strip().strip(',') + '\n')
    output.close()
    return columnNames

def writeCharacteristicToFile(lb, ColumnNames, content):
    head = '<td valign="top" align="left">'
    tail = '</td>'
    start = 0
    n = 0
    output = open('./basics/character.csv', 'a')
    output.write(lb + ',')
    for name in ColumnNames:
        str = head+name+tail
        start = content.find(str, 0)
        begin = content.find(head, start + len(str))
        begin += len(head)
        end = content.find(tail,begin)
        val = content[begin:end]
        val = val.replace('\n', ' ')
        if n != 0:
            output.write(',')
        if(len(val)!=0):
            output.write(val)
        else:
            output.write('NULL')
        n = n + 1
    output.write("\n")
    output.close()
