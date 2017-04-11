import re
import os
import codecs


def extractTitle(fileName):
    fo = codecs.open(fileName, 'r')

    font_pattern = re.compile(r'font="(.+?)"')
    size_pattern = re.compile(r'size="(.+?)"')
    content_pattern = re.compile(r'>(.)</text>', re.M)

    labelsList = []
    label = ''
    for line in fo:
        flag = 0
        if len(font_pattern.findall(line)) != 0 and len(size_pattern.findall(line)) != 0 and len(
                content_pattern.findall(line)):
            flag = 1

        if flag == 1 and font_pattern.findall(line)[0] in ('TimesNewRomanPS-BoldMT', 'TimesNewRoman,Bold') and \
            13.0 <= float(size_pattern.findall(line)[0]) <= 14.0:
            label += content_pattern.findall(line)[0]
        else:
            label = label.strip()
            if len(label) != 0:
                labelsList.append(label)
            label = ''
    labelsList = [item for item in labelsList if 'A' <= item[0] <= 'Z']
    return labelsList
