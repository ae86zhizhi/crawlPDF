import re
import os
import codecs

def process(str):
    str = str.replace('\t', '')
    str = str.replace('<br>', '')
    str = str.replace(' &nbsp; ', ' ')
    str = str.strip()
    str = str.replace('\n\n', '; ')
    return str
#一共就6个属性，我就不提供属性名了,输入是html文件
def getProfile(content):
    symbol_pattern = re.compile(r'<td valign="top"><strong>Symbol:</strong></td>.+?<td valign="top">(.+?)</td>',re.S)
    symbol = symbol_pattern.findall(content)[0]
    #print(process(symbol))
    group_pattern = re.compile(r'<td valign="top"><strong>Group:</strong></td>.+?<td valign="top">(.+?)	</td>', re.S)
    group = group_pattern.findall(content)[0]
    #print(process(group))
    family_pattern = re.compile(r'<td valign="top"><strong>Family:</strong></td>.+?<td valign="top">(.+?)	</td>', re.S)
    family = family_pattern.findall(content)[0]
    #print(process(family))
    duration_pattern = re.compile(r'<td valign="top"><strong>Duration:</strong></td>.+?<td valign="top">(.+?)	</td>',re.S)
    duration = duration_pattern.findall(content)[0]
    #print(process(duration))
    growth_habit_pattern = re.compile(r'<strong>Growth.+?Habit</strong></a><strong>:</strong></td>.+?<td valign="top">(.+?)</td>',re.S)
    growth_habit = growth_habit_pattern.findall(content)[0]
    #print(process(growth_habit))
    native_status_pattern = re.compile(r'<strong>Native.+?Status</strong></a><strong>:</strong></td>.+?<td valign="top">(.+?)</td>', re.S)
    native_status = native_status_pattern.findall(content)[0]
    #print(process(native_status))
    ##写入这个文件，自己改
    output = open("profile.csv","a")
    output.write('\''+process(symbol)+'\',\''+process(group)+'\',\''+process(family)+'\',\''+process(duration)+'\',\''+process(growth_habit)+'\',\''+process(native_status)+'\'\n')
    output.close()

def main():
    fo = codecs.open("F:\\Profile.html", 'r', 'utf-8')
    c = fo.read();
    getProfile(c)
    fo.close()


if __name__ == '__main__':
    main()