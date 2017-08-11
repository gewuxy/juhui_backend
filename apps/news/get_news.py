# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import traceback
import re

NEWS_FROM1 = 'http://www.wines-info.com/'
NEWS_FROM2 = 'http://www.lookvin.com/news/'
NEWS_FROM3 = 'https://www.putaojiu.com/news/'
NEWS_FROM4 = 'http://www.wine-world.com/culture/zx'
NEWS_FROM5 = 'http://www.vinehoo.com/index.php/Home/News/index.html'
NEWS_FROM6 = 'https://www.winesou.com/toutiao/'
NEWS_SAVE = 'https://jh.qiuxiaokun.com/api/news/insert/'
# NEWS_SAVE = 'http://127.0.0.1:9991/api/news/insert/'


def get_news1():
    '''
    从NEWS_FROM1中爬取葡萄酒资讯信息，并存入数据库中
    '''
    r_index = requests.get(NEWS_FROM1)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all(attrs={"class": "news-list new-hot"})
    if not index_tags:
        return False
    for content in index_tags[0].ul.contents:
        try:
            if content == '\n':
                continue
            title = content.a.string.strip()
            href = content.a['href']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            article_tags = soup_page.find_all(attrs={"class": "article-details-info"})
            article = str(article_tags[0])
            img = article_tags[0].find('img')
            if not img:
                continue
            thumb_img = img['src']
            time_tags = soup_page.find_all(attrs={"class": "release-author"})
            time_origin_author = time_tags[0].div.contents
            news_time = time_origin_author[1].string
            origin = time_origin_author[3].string
            author = time_origin_author[5].string

            data = {
                'title': title,
                'href': href,
                'thumb_img': thumb_img,
                'news_time': news_time,
                'article': article,
                'origin': origin,
                'author': author
            }
            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))
        except Exception:
            traceback.print_exc()
            continue


def get_news2():
    '''
    从NEWS_FROM2中爬取葡萄酒资讯信息，并存入数据库中
    :return:
    '''
    r_index = requests.get(NEWS_FROM2)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all(attrs={"class": "news-list"})
    if not index_tags:
        return False
    for content in index_tags[0].contents:
        try:
            if content == '\n':
                continue
            title = content.dd.img['alt']
            href = content.dd.a['href']
            img = content.dd.img['src']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            meta_tags = soup_page.find_all(attrs={"class": "page-meta"})
            news_time = meta_tags[0].contents[1].string[:-3]
            print(news_time)
            origin = meta_tags[0].contents[3].string
            author = meta_tags[0].contents[5].string
            content_tags = soup_page.find_all(attrs={"class": "page-content"})
            article = str(content_tags[0])

            data = {
                'title': title,
                'href': href,
                'thumb_img': img,
                'news_time': news_time,
                'article': article,
                'origin': origin,
                'author': author
            }

            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))

        except Exception:
            traceback.print_exc()
            continue


def get_news3():
    '''
    从NEWS_FROM3中爬取葡萄酒资讯信息，并存入数据库中
    '''
    r_index = requests.get(NEWS_FROM3)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all(attrs={"class": "wz-list tab-box"})
    if not index_tags:
        return False
    for content in index_tags[0].ul.contents:
        try:
            if content == '\n':
                continue
            title = content.div.a['title']
            href = content.div.a['href']
            img = content.div.img['src']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            time_tags = soup_page.find_all(attrs={"class": "wz-item1 clearfix"})
            news_time = time_tags[0].contents[1].string
            origin = '葡萄酒网'
            author_tags = soup_page.find_all('span', {'class': 'fr'})
            author = author_tags[0].string.split('：')[1][:-1]
            content_tags = soup_page.find_all(attrs={"class": "wz-item3"})
            article = str(content_tags[0])

            data = {
                'title': title,
                'href': href,
                'thumb_img': img,
                'news_time': news_time.strip(),
                'article': article,
                'origin': origin,
                'author': author
            }
            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))

        except Exception:
            traceback.print_exc()
            continue


def get_news4():
    '''
    从NEWS_FROM4中爬取葡萄酒资讯信息，并存入数据库中
    '''
    r_index = requests.get(NEWS_FROM4)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all(attrs={"class": "atList"})
    if not index_tags:
        return False
    reTIME = re.compile('(\d+?)年(\d+?)月(\d+?)日 (\d+?):(\d+?):\d+')
    for content in index_tags[0].contents:
        try:
            if content == '\n':
                continue
            title = content.dt.a['title']
            href = content.dt.a['href']
            img = content.dt.img['realsrc']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            time_tags = soup_page.find_all('span', {'id': 'wkTime'})
            news_time = time_tags[0].contents[0].string.strip()
            t = reTIME.search(news_time)
            news_time = '{0}-{1}-{2} {3}:{4}'.format(
                t.group(1), t.group(2).zfill(2), t.group(3).zfill(2),
                t.group(4).zfill(2), t.group(5).zfill(2))
            origin = '红酒世界网'
            author = ''
            content_tags = soup_page.find_all(attrs={"class": "wkBody"})
            abstract_tag = content_tags[0].div.extract()
            version_tag = content_tags[0].div.extract()
            article = str(content_tags[0])

            data = {
                'title': title,
                'href': href,
                'thumb_img': img,
                'news_time': news_time,
                'article': article,
                'origin': origin,
                'author': author
            }
            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))

        except Exception:
            traceback.print_exc()
            continue


def get_news5():
    '''
    从NEWS_FROM5中爬取葡萄酒资讯信息，并存入数据库中
    '''
    r_index = requests.get(NEWS_FROM5)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all(attrs={"class": "blog-list"})
    if not index_tags:
        return False
    for content in index_tags[0].contents:
        try:
            if content == ' ':
                continue
            title = content.div.a['title']
            href = 'http://www.vinehoo.com/' + str(content.div.a['href'])
            img = content.div.img['src']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            detail_tags = soup_page.find_all(attrs={"class": "content-detial-info"})
            info_list = list(detail_tags[0].stripped_strings)
            news_time = info_list[0][-19:-3]
            origin = info_list[1].split('：')[1]
            author = info_list[2].split('：')[1]
            content_tags = soup_page.find_all(attrs={"class": "content-detial-content"})
            article = str(content_tags[0])

            data = {
                'title': title,
                'href': href,
                'thumb_img': img,
                'news_time': news_time,
                'article': article,
                'origin': origin,
                'author': author
            }
            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))

        except Exception:
            traceback.print_exc()
            continue


def get_news6():
    '''
    从NEWS_FROM6中爬取葡萄酒资讯信息，并存入数据库中
    '''
    r_index = requests.get(NEWS_FROM6)
    if r_index.status_code != 200:
        return False
    soup_index = BeautifulSoup(r_index.content, 'html.parser')
    index_tags = soup_index.find_all('ul', {'id': 'toutiao-content'})
    if not index_tags:
        return False
    for content in index_tags[0].contents:
        try:
            if content == '\n':
                continue
            title = content.div.div.a['title']
            href = content.div.div.a['href']
            img = content.div.div.img['src']
            r_page = requests.get(href)
            if r_page.status_code != 200:
                continue
            soup_page = BeautifulSoup(r_page.content, 'html.parser')
            detail_tags = soup_page.find_all(attrs={"class": "Ws-MessConTop Ws-BgBai clearfix"})
            info_list = list(detail_tags[0].stripped_strings)
            news_time = info_list[2]
            origin = info_list[5]
            if origin == '\ue60f':
                origin = '酒一搜'
                author = info_list[6].split('：')[1]
            else:
                author = info_list[7].split('：')[1]
            content_tags = soup_page.find_all(attrs={"class": "Ws-MessConText Ws-BgBai"})
            article = str(content_tags[0])

            data = {
                'title': title,
                'href': href,
                'thumb_img': img,
                'news_time': news_time,
                'article': article,
                'origin': origin,
                'author': author
            }
            r_save = requests.post(NEWS_SAVE, data=data)
            print('save news result is {0}'.format(r_save.content))

        except Exception:
            traceback.print_exc()
            continue

if __name__ == '__main__':
    get_news1()
    get_news2()
    get_news3()
    get_news4()
    get_news5()
    get_news6()
