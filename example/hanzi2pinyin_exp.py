'''
利用python的pypinyin，将中文转换为拼音的各种常见函数使用示例。
'''
from pypinyin import pinyin, lazy_pinyin, Style

def Hanzi2Pinyin(word):
    py = pinyin(word, heteronym=False)  # 设置heteronym=True输出多音字读音。
    print("普通拼音:", py)

    py = pinyin(word, heteronym=True)
    print("开启多音字拼音:", py)

    py = pinyin(word, style=Style.FIRST_LETTER)
    print("拼音首字母:", py)

    # lazy_pinyin,获取输入句子的不带声调的拼音list。
    py = lazy_pinyin(word)
    print("不考虑多音字和声调拼音:", py)

    # 设置error参数：
    # default: 不处理其他字符，直接返回
    # ignore: 忽略不包含拼音的字符
    py = lazy_pinyin(word + '→※❤' + 'add', errors='ignore')
    print("忽略不包含拼音的字符:", py)

    py = lazy_pinyin(word, style=Style.TONE3)
    print("拼音后面用数字表示声调:", py)

if __name__ == "__main__":
    word = '中意，重庆'
    Hanzi2Pinyin(word)
