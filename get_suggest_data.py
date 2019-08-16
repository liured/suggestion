import pandas as pd
import string
import re

def find_chinese(file):
    '''
    获取输入的中文字符。
    :param file:
    :return: 输入中的中文字符
    '''
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese

def get_words_set():
    '''
    获取查询推荐补全词。
    :return: 所有的查询推荐词条set。
    '''

    return words_set

def get_words_score():
    '''
    从日志文件中，获取历史关键词条及该词条对应的归一化查询概率。
    :return: 返回dictionary{查询词：查询概率}
    '''

    return word_score
