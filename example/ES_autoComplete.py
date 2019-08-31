'''
Elasticsearch自动补全示例。
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch_dsl import connections, Document, Text, Keyword, Completion, analyzer, Float

connections.create_connection(hosts=["localhost"], timeout=30) # 创建连接，默认为localhost,端口5000 （http://127.0.0.1:5000/）

class SuggestLive(Document):
    subject = Text()
    content = Text()  # 文档内容
    weight = Float()  # 浮点数权重
    suggest_word = Completion()  # 自动补全的字段
    class Index:
        name = 'suggest_index'

    def save(self, ** kwargs):
        return super(SuggestLive, self).save(** kwargs)

SuggestLive.init()  # elasticsearch中创建mapping

def add_live(id_, query, content, weight):
    live = SuggestLive(meta={'id': id_})
    live.subject = query
    live.content = content
    live.suggest_word = query
    live.weight = weight
    live.save()

def init_data():
    add_live(1,'机器学习',  '支持向量机是一种传统的机器学习算法', 0.01)
    add_live(2,'深度学习', '近几年来，越来越多的深度学习算法应用在，无论在学术界还是业界。', 0.2)
    add_live(3, 'machine learning', 'this is a description about',0.005)
    add_live(4, '智能机器', 'AI', 0.07)
    add_live(5, '运动机器', '在国家举办的足球机器人比赛',0.003)
    add_live(6,'机动器械', '一种工具。',0.0001)

def ES_suggest(key):
    s = SuggestLive.search()
    s = s.suggest('my_suggestion', key,
                  completion={'field': 'suggest_word', 'fuzzy': {'fuzziness': 2, 'prefix_length': 2}, 'size': 10})
    suggestions = s.execute()
    for match in suggestions.suggest.my_suggestion[0].options:
        source = match._source
        print('--------------------------')
        print(source['subject'],source['content'],source['weight']) #, match._score

if __name__ == '__main__':
    init_data()
    ES_suggest('机器')
