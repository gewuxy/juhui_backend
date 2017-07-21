# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import traceback

NEWS_FROM = 'http://www.wines-info.com/'
NEWS_SAVE = 'https://jh.qiuxiaokun.com/api/news/insert/'


def get_news():
    r_index = requests.get(NEWS_FROM)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all(attrs={"class": "news-list new-hot"})
    if not index_tags:
        return False
    title = ''  # 标题
    href = ''  # 链接
    thumb_img = ''  # 缩略图
    news_time = ''  # 信息源时间
    try:
        for content in index_tags[0].ul.contents:
            if content == '\n':
                continue
            title = content.a.string.strip()
            href = content.a['href']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            article_tags = soup_page.find_all(attrs={"class": "article-details-info"})
            img = article_tags[0].find('img')
            if not img:
                continue
            thumb_img = img['src']
            time_tags = soup_page.find_all(attrs={"class": "release-author"})
            news_time = time_tags[0].div.span.string

            data = {
                'title': title,
                'href': href,
                'thumb_img': thumb_img,
                'news_time': news_time
            }
            print(data)
            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))
    except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    get_news()