from flask import Flask, redirect, url_for, render_template, request, flash
from api import News
from api import Keyword
from api import Url
from api import Category
from time import time

app = Flask(__name__)
result = {}


@app.route("/")
def home():
    return render_template("index2.html", result=result)


def compare_and_remove(dict_ans):
    pass


def process(url, key):
    categorys = Category()
    list_category = []
    for url_home in url.list_url:
        list_category += categorys.get_category_url_from_url(url_home)
    list_category
    start = time()
    news = News()
    print(f'time1 : {time()-start}')
    news.load_urls(list_category)
    print(f'time2 : {time()-start}')
    news.load_text()
    print(f'time3 : {time()-start}')
    news.load_key()
    print(f'time4 : {time()-start}')
    news.load_score(key.list_keys)
    print(f'time5 : {time()-start}')
    print('list text ', len(news.list_text_news))
    print('list counter key ', len(news.list_counter_keys))
    print('list score ', len(news.list_score_news))
    print('list title ', len(news.list_title))
    print('list url ', len(news.list_url_news))
    list_ans = news.list_score_news

    # for i in range(len(news.list_url_news)):
    #     print(news.list_url_news[i])
    #     print(news.list_title[i])

    list_index=[_ for _ in range(len(list_ans))]
    dict_ans=dict(zip(list_ans, list_index))
    dict_ans=dict(sorted(dict_ans.items(), key=lambda x: -x[0])[:20])
    print(dict_ans)

    dict_res={}
    for _, i in dict_ans.items():
        dict_res[news.list_title[i]]=(news.list_url_news[i], news.list_title[i])
    # print(dict_res)
    print('total time : ', time()-start)
    return dict_res


@ app.route("/", methods=["POST", "GET"])
def crawl():
    list_urls=[1, 2, 3]
    list_keys=[1, 2, 3]
    if request.method == 'POST':
        list_urls[0]=request.form['url0']
        list_urls[1]=request.form['url1']
        list_urls[2]=request.form['url2']
        list_keys[0]=request.form['key0']
        list_keys[1]=request.form['key1']
        list_keys[2]=request.form['key2']

        urls=Url(list_urls)
        urls.standardized()
        keys=Keyword(list_keys)
        keys.standardized()
        result=process(urls, keys)
        print(type(result))
        # result = {'test1': 'pham hong thai', 'test2': 'thaiph99'}

    return render_template('index2.html', result=result)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8020)
