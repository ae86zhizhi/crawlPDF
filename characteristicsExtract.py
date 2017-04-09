import re
import os
import codecs
fo = codecs.open("F:\\PLANTS.html",'r','utf-8')

#characteristic_pattern1 = re.compile(r'<tr>........<td valign="top" align="left">(.+?)</td>........<td valign="top" align="left">(.+?)</td>......</tr>',re.S)

def writeCharacteristicToFile(content):
    col_names = getColumnNames(content)
    output = open('lieming.csv', 'a')
    str =''
    n = 0
    for name in col_names:
        name.strip()
        name.replace(' ','_')
        #还要替换哪些自己写
        if n != 0:
            str += ','
        str += name
    output.write(str)

#输入html，返回一个列名的list
def getColumnNames(content):
    characteristic_pattern = re.compile(r'<tr>........<td valign="top" align="left">(.+?)</td>.+?</tr>', re.S)
    col_name = characteristic_pattern.findall(content);
    return col_name
#输入列名的list和html，将值写入文件
def writeCharacteristicToFile(ColumnNames, content):
    head = '<td valign="top" align="left">'
    tail = '</td>'
    start = 0;
    n =0;
    output = open('kengdie.csv', 'a')
    for name in ColumnNames:
        str = head+name+tail
        start = content.find(str, 0)
        begin = content.find(head, start + len(str))
        begin += len(head)
        end = content.find(tail,begin)
        val = content[begin:end]
        if n != 0:
            output.write(",")
        if(len(val)!=0):
            output.write("\'"+val+"\'")
        else:
            output.write("NULL")
        n = n + 1
    output.write("\n")
    output.close()

def main():
    fo = codecs.open("F:\\PLANTS.html", 'r', 'utf-8')
    c = fo.read();
    writeCharacteristicToFile(getColumnNames(c),c)
    fo.close()


if __name__ == '__main__':
    main()