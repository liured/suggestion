'''
简单的倒排索引构建示例。
'''
import jieba
import pprint

def get_forward_dict():
    '''
    返回文档id-->关键词的正向索引。
    :return:
    '''
    docs = ['林俊杰2019年圣所演唱会门票','容祖儿与林俊杰在演唱会上合唱歌曲燃爆全场','2019年黄牛手中购买演唱会门票']
    doc_dict = {}
    for i, doc in enumerate(docs):
        word_list = list(jieba.cut_for_search(doc))
        doc_dict[i] = word_list
    pprint.pprint(doc_dict)
    return doc_dict

def create_invert_index(doc_dict):
    '''
    构建倒排索引。
    :param doc_dict:
    :return:
    '''
    invert_index = {}
    for id, words in doc_dict.items():
        for word in words:
            if word not in invert_index.keys():
                invert_index[word] = []
            invert_index[word].append(id)
    pprint.pprint(invert_index)
    return invert_index

if __name__ == "__main__":
    create_invert_index(get_forward_dict())
