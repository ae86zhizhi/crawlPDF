# -*- coding:utf-8 -*-

def extract_string(content, begin_pattern, end_pattern, pos):
    return content[content.find(begin_pattern, pos) + len(begin_pattern): content.find(end_pattern, pos + 1)].replace('\n', ' ')

def text_to_sql(content):
    return content.replace("\\", "\\\\").replace("'", "\\'")

def textToIdentifier(content):
    x = ''
    content = content.replace('\n', ' ').strip().strip(':')
    for i in range(0, len(content)):
        if not ('A' <= content[i] <= 'Z') and not ('a' <= content[i] <= 'z') and not ('0' <= content[i] <= '9') and content[i] != '_':
            x += '_'
        else:
            x += content[i]
    return x