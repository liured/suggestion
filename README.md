# suggestion
   ElasticSearch + Flask实现搜索关键词自动补全功能demo。（利益相关，省略简化了输入数据function）
## 介绍
   基于elasticsearch和flask实现搜索引擎自动补全（前缀匹配）功能，支持中文、英文、拼音（简拼/全拼）->中文的补全。

<a href="https://www.zhihu.com/people/liured-30/posts" target="_blank">搜索查询自动补全方法介绍</a>

## 解决方案
1. 查询补全数据来源：
   利用搜索日志，统计挖掘用户历史搜索热词，按照查询词的搜索次数（归一化的权重）作为自动补全排序的依据；
2. 中英文补全：
   基于ES的suggest功能实现中文和英文的自动补全，模糊搜索；
3. 拼音补全：
   通过搜索日志获取了补全数据后，将中文转化为拼音全拼、首拼。构建拼音->中文的倒排索引进行检索。用户输入的查询，首先进行拼音检测，检测到拼音则检索该拼音对应的中文关键词列表，根据返回的中文关键词继续检索相关补全数据，利用权重排序后展示给用户。
4. 用户个性化：
   加到用户点击过的历史查询词的权重，当下一次用户再次查询该词时，由于权重增加优先排在前面展示。


## 使用说明
   - Python 3.7 + JDK 1.8
   - 下载elasticsearch-7.3.0版本
   - 安装 Flask-1.1.1版本
   - 安装elasticsearch-dsl

## 相关技术
- ES的简单使用
- 汉字转拼音
- 倒排索引
- Flask的简单使用

<a href="https://zhuanlan.zhihu.com/p/80581588" target="_blank">查询推荐Demo实战相关技术</a>
