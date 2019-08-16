from flask import Flask, request, render_template, jsonify
from elasticsearch_dsl import connections, Document, Text, Keyword, Completion, analyzer, Long, Float, token_filter,Q,Search
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from hanzi2pinyin import get_Invert_Index
from get_suggest_data import get_words_score

def search_PinYin(input_pinyin, invert_index):
    trans_word_lst = None
    if input_pinyin in invert_index.keys():
        trans_word_lst = invert_index[input_pinyin]
    if trans_word_lst:
        print(trans_word_lst)
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
    s = BlogLive.search().sort('weight', '-weight')
    #  prefix_length: 不检查模糊匹配的最小长度，默认=1；
    #  fuzziness： 允许模糊匹配，利用编辑距离来推断；
    s = s.suggest('live_suggestion', key,
                  completion={'field': 'live_suggest', 'fuzzy': {'fuzziness': 2, 'prefix_length': 2}, 'size': 10})
    suggestions_w = s.execute()
    suggest_list_1 = []

    for match in suggestions_w.suggest.live_suggestion[0].options:
        source = match._source
        suggest_list_1.append((source['subject'], float(source['weight'])))
    return suggest_list_1

def my_update(word, score):
    # q = Q('bool',must=[Q('match',live_suggest=word), Q('match',weight=score)])
    q = Q('bool', must=[Q('match', live_suggest=word)])
    s=Search().query(q)
    response = s.execute()
    if response.success():
        h = response.hits[0]
        print(h)
        my_id = h.meta.id
        add_live(my_id,word,score+0.5)

def my_suggest(key):
    suggest_list = []
    pinyin_key_lst = search_PinYin(key, invert_index)
    if pinyin_key_lst:
        suggest_list_1 = []
        for pinyin_key in pinyin_key_lst:
            suggest_list_1.extend(es_suggest(pinyin_key))
        print('########## 来自拼音')
        # 通过拼音推荐补全词
        suggest_list_1 = sorted(suggest_list_1, key=lambda w: w[1], reverse=True)
        print(suggest_list_1)
        k_set = set()
        for item in suggest_list_1:
            if item[0] not in k_set:
                suggest_list.append({'value':item[0] +  '-' + str(item[1]), 'weight':item[1]})
                k_set.add(item[0])
    else:
        # 中英文补全
        suggest_list_1 = es_suggest(key)
        print('########## 来自ES')
        suggest_list_1 = sorted(suggest_list_1, key=lambda w: w[1], reverse=True)
        print(suggest_list_1)
        k_set = set()
        for item in suggest_list_1:
            if item[0] not in k_set:
                suggest_list.append({'value':item[0] + '-' + str(item[1]), 'weight':item[1]})
                k_set.add(item[0])

    return suggest_list

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/search/<string:box>")
def process(box):
    query = request.args.get('query')
    print(query)
    if box == 'suggests':
        suggestions = my_suggest(query)
    return jsonify({"suggestions":suggestions})

@app.route("/",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        word_score = request.form['suggests']
        word, score = word_score.split('-')[0], word_score.split('-')[1]
        print('get word ==================',word, score)
        my_update(word, float(score))
    return render_template('result.html',word=word)

if __name__ == "__main__":
    connections.create_connection(hosts=["localhost"], timeout=30)
    BlogLive.init()
    invert_index = get_Invert_Index()
    words_score_set = get_words_score()
    id = init_data(words_score_set)
    # id = id-1
    app.run(debug=True)
