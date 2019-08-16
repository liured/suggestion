from flask import Flask, request, render_template, jsonify
from elasticsearch_dsl import connections, Document, Text, Keyword, Completion, analyzer, Long, Float, token_filter,Q,Search
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from hanzi2pinyin import get_Invert_Index
from get_suggest_data import get_words_score

def search_PinYin(input_pinyin, invert_index):
 ...
    return trans_word_lst

class CustomAnalyzer(_CustomAnalyzer):
    """
        避免ik_analyzer参数传递时会报错的问题
    """
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class BlogLive(Document):
    subject = Text()
    weight = Float()
    topics = Keyword()
    live_suggest = Completion()
    class Index:
        name = 'blog'

    def save(self, ** kwargs):
        return super(BlogLive, self).save(** kwargs)

def add_live(id_, subject, weight):
    live = BlogLive(meta={'id': id_})
    live.subject = subject
    live.live_suggest = subject
    live.weight = weight
    live.save()

def init_data(words_score_set):
    # add_live(1, '这里是文本', 0.001)
    id = 1
    for k,v in words_score_set.items():
        add_live(id, k, v)
        id += 1
    return id

def es_suggest(key):
    '''
    利用elasticsearch_dsl，返回key的自动补全列表。

    :param key: 用户输入的关键词
    :return: 来自ES的自动补全列表。
    '''
...
    return suggest_list_1

def my_update(word, score):
 ...

def my_suggest(key):
   ...
    return suggest_list

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/search/<string:box>")
...
    return jsonify({"suggestions":suggestions})

@app.route("/",methods=['GET','POST'])
def login():
   ...
    return render_template('result.html',word=word)

if __name__ == "__main__":
    connections.create_connection(hosts=["localhost"], timeout=30)
    BlogLive.init()
    invert_index = get_Invert_Index()
    words_score_set = get_words_score()
    id = init_data(words_score_set)
    # id = id-1
    app.run(debug=True)
