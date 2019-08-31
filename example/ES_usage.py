'''
Elasticsearch的简单实用，包括插入、更新、删除、查询操作。
'''
from elasticsearch import Elasticsearch

def Insert(data):
    es = Elasticsearch()
    es.create(index='my_index', doc_type='test_type', id=11, body=data) # create()方法创建index为索引名称，doc_type为文档类型，id为数据的唯一标识，body为文档的内容（json格式）
    res = es.get(index="my_index", doc_type="test_type", id=11)

    print('插入数据: \n')
    print(res)

def Update(up_data):
    es = Elasticsearch()
    es.update(index='my_index', doc_type='test_type', id=11, body=up_data)
    res = es.get(index='my_index', doc_type='test_type', id=11)    # res 为<class 'dict'>
    # 查看文章中的更新后的name。
    print('更新后的数据为：\n'+res['_source']['name'])
    # print(res)
    " {'_index': 'my_index', '_type': 'test_type', '_id': '11', '_version': 2, '_seq_no': 12, '_primary_term': 1, 'found': True, '_source': {'name': 'xiaoming', 'add': '广东省'}} "

def Delete():
    es = Elasticsearch()
    es.delete(index='my_index', doc_type='test_type', id=11)
    print('删除数据 \n')

def Search():
    es = Elasticsearch()
    query_all = es.search(index='my_index', body={"query":{"match_all":{}}})
    print('输出所有的查询: ')
    print(query_all)

    query_n = es.search(index='my_index', body={"query":{"term":{"name":"xiao_ming"}}})
    print('输出name=xiao_ming的查询: ')
    print(query_n['hits']['hits'][0])


data = {"name":"python", "add":"广东省"}
up_data = {"doc":{"name":"xiao_ming", "add":"广东省"}}
