import re
import os
import codecs


def extractTitle(fileName):
    fo = codecs.open(fileName, 'r')

    font_pattern = re.compile(r'font="(.+?)"')
    size_pattern = re.compile(r'size="(.+?)"')
    content_pattern = re.compile(r'>(.)</text>', re.M)
    str = ['<text font="TimesNewRomanPS-BoldMT" bbox="72.000,247.916,79.234,261.272" size="13.357">U</text>',
           '<text font="TimesNewRomanPS-BoldMT" bbox="79.239,247.916,83.137,261.272" size="13.357">s</text>',
           '<text font="TimesNewRomanPS-BoldMT" bbox="83.142,247.916,87.591,261.272" size="13.357">e</text>',
           '<text font="TimesNewRomanPS-BoldMT" bbox="87.596,247.916,91.494,261.272" size="13.357">s</text>',
           '<text font="TimesNewRomanPS-BoldMT" bbox="91.499,247.916,94.004,261.272" size="13.357"> </text>']
    labelsList = []
    label = ''
    for line in fo:
        flag = 0
        if len(font_pattern.findall(line)) != 0 and len(size_pattern.findall(line)) != 0 and len(
                content_pattern.findall(line)):
            flag = 1

        if flag == 1 and font_pattern.findall(line)[0] == 'TimesNewRomanPS-BoldMT' and 13.0 <= float(size_pattern.findall(line)[
            0]) <= 14.0:
            label += content_pattern.findall(line)[0]
        else:
            label = label.strip()
            if len(label) != 0:
                labelsList.append(label)
            label = ''
    labelsList = [item for item in labelsList if item[0] >= 'A' and item[0] <= 'Z']
    return labelsList
