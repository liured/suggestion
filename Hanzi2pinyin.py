from pypinyin import pinyin, lazy_pinyin
import pypinyin
from get_suggest_data import get_words_set, find_chinese

def Hanzi2Pinyin(word):
    '''
    获取汉字对应的全拼、首拼、第一拼。
    :param word:
    :return:
    '''
    quan_pin = lazy_pinyin(word)
    quan_pin_str = ''
    for qp in quan_pin:
        quan_pin_str += qp
    first_letter = pinyin(word, style=pypinyin.FIRST_LETTER)
    first_letter_str = ''
    for fl in first_letter:
        first_letter_str += fl[0]

    return [quan_pin[0], quan_pin_str, first_letter_str]

def get_Invert_Index():
    '''
    构建拼音倒排索引并返回。
    :return:
    '''
    # 构建 中文-->拼音列表 字典
    # 例如：[{'浏览器': ['liu', 'liulanqi', 'llq']}, {'告白气球': ['gao', 'gaobaiqiqiu', 'gbqq']}]
    words_set = get_words_set()
    words_set_pinyin = {}
    for word in words_set:
        if find_chinese(str(word)) and len(word)<6:
            pinyin_lst = Hanzi2Pinyin(word)
            words_set_pinyin[word] = pinyin_lst

    # 构建所有拼音的集合.
    pinyin_key_set = set()
    for key, values in words_set_pinyin.items():
        for v in values:
            pinyin_key_set.add(v)

    # 构建倒排索引.
    invert_index = dict()
    for py_key in pinyin_key_set:
        tmp = []
        for my_word, my_pinyin in words_set_pinyin.items():
            if py_key in my_pinyin:
                tmp.append(my_word)
        invert_index[py_key] = tmp

    # 额外添加热词的首个字符的首拼
    # 例如 {'n'：['哪吒','哪吒票房']}
    extra = {}
    for k,v in extra.items():
        invert_index[k] = v
    # print(invert_index)
    return invert_index

if __name__ == "__main__":
    word = "哪吒"
    print(Hanzi2Pinyin(word))
    print(find_chinese('哪吒piaofang'))
