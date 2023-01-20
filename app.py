import os
import json
import platform
import pathlib
import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data/")

app = Flask(__name__)


@app.route('/api')
def api():
    kategori = ['detikcom', 'news', 'finance', 'hot', 'inet', 'sport', 'oto', 'travel', 'sepakbola', 'food', 'health',
                'wolipop']

    cat = request.args.get('cat') or 'detikcom'
    update = request.args.get('update') or False

    if update:
        if cat == 'all':
            print('updating all..')
            for kat in kategori:
                get_populer(kat)
            print('update all done!')
        else:
            get_populer(cat)
            print('update {} done!'.format(cat))

    if cat == 'all':
        cat = "detikcom"
    populer_posts = load_populer(cat)

    fname = pathlib.Path('{}detik-{}.json'.format(DATA_DIR, cat))
    mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
    up_time = mtime.strftime("%d %b %H:%M")

    data = {
        'length': len(populer_posts),
        'posts' : populer_posts,
        'update_time': up_time,
        'cat': cat,
        'categories': kategori
    }

    return data

    
@app.route('/')
def home():
    kategori = ['detikcom', 'news', 'finance', 'hot', 'inet', 'sport', 'oto', 'travel', 'sepakbola', 'food', 'health',
                'wolipop']

    cat = request.args.get('cat') or 'detikcom'
    update = request.args.get('update') or False

    newurl = request.args.get('url') or False



    if update:
        if cat == 'all':
            print('updating all..')
            for kat in kategori:
                get_populer(kat)
            print('update all done!')
        else:
            get_populer(cat)
            print('update {} done!'.format(cat))

    if cat == 'all':
        cat = "detikcom"
    populer_posts = load_populer(cat)

    fname = pathlib.Path('{}detik-{}.json'.format(DATA_DIR, cat))
    mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
    up_time = mtime.strftime("%d %b %H:%M")

    if newurl:
        print("newurl", newurl)
        scrapped = get_scrap(newurl)
        populer_posts= scrapped


    return render_template('detik-terpopuler.html', populers = populer_posts, kategori = kategori, now = cat,
                           up_time=up_time)


def get_populer(cat):
    print('update {}'.format(cat), end='')

    url = 'https://www.detik.com/terpopuler/' + cat
    soup = BeautifulSoup(requests.get(url).text, features='html.parser')
    populer_area = soup.find(attrs={'class': 'grid-row list-content'})
    populers = populer_area.findAll(attrs={'class': 'media__image'})

    # populers = populers[:1]
    populer_posts = []
    populer_json = []

    for id_post, judul in enumerate(populers):
        url_post = judul.find('a')['href']
        post_soup = BeautifulSoup(requests.get(str(url_post) + '?single=1').text, features='html.parser')
        try:
            post_content = post_soup.find(attrs={'class': 'itp_bodycontent'})
        except:
            pass
        populer_posts.append([judul, post_content, id_post])

        data_post = {
            'title': judul.find('a').find('img')['title'],
            'img' : judul.find('a').find('img')['src'],
            'content': '"{}"'.format(post_content),
            'id': id_post,
            'url_post':url_post
        }
        populer_json.append(data_post)
        print('.',end='')

    print('download {} done!'.format(cat))

    with(open('{}detik-{}.json'.format(DATA_DIR, cat), 'w')) as fl:
        json.dump(populer_json, fl)

def get_scrap(url):
    print('get news from url: {}'.format(url))

    try:

        url_post = url

        if "detik.com" in url_post:        
            post_soup = BeautifulSoup(requests.get(str(url_post) + '?single=1').text, features='html.parser')
            try:
                post_title = post_soup.find(attrs={'class': 'detail__title'}).text.strip()
                post_img = post_soup.find(attrs={'class': 'detail__media'}).find('figure').find('img')['src']
                post_content = post_soup.find(attrs={'class': 'itp_bodycontent'})
            except:
                raise Exception("detik gagal parse")
                print("gagal parse detik")
                # pass
        # populer_posts.append([judul, post_content, id_post])

        if "tribunnews.com" in url_post:        
            post_soup = BeautifulSoup(requests.get(str(url_post)).text, features='html.parser')
            try:
                print(post_soup)
                post_title = post_soup.find(attrs={'id': 'article'}).find('h1').text.strip()
                print(post_title, post_title)
                post_img = post_soup.find(attrs={'class': 'detail__media'}).find('figure').find('img')['src']
                post_content = post_soup.find(attrs={'class': 'itp_bodycontent'})
            except:
                raise Exception("tribunnews gagal parse")
                print("gagal parse detik")
                # pass
        # populer_posts.append([judul, post_content, id_post])

        #https://herstory.co.id/read111635/cek-fakta-sudah-tak-kuat-menahan-nikita-mirzani-syok-tiba-tiba-sule-lumat-organ-intimnyaastaga?page=all
        if "herstory.co.id" in url_post:        
            post_soup = BeautifulSoup(requests.get(str(url_post) + '?page=all').text, features='html.parser')
            try:
                # print(post_soup)
                post_title = post_soup.find('h2', attrs={'class': 'fw-bolder'}).text.strip()
                print(post_title, post_title)
                post_img = post_soup.find('picture').find('source')['srcset']
                print(post_title, post_title)

                post_content = post_soup.find(attrs={'class': 'article-post'})
                # print(post_content, post_content)
            except:
                raise Exception("herstory gagal parse")
                print("gagal parse detik")
                # pass
        # populer_posts.append([judul, post_content, id_post])

        data_post = {
            'title': post_title,
            'img' : post_img,
            'content': '"{}"'.format(post_content),
            'id': 1,
            'url_post':url_post
        }
        
        print("data_post")
        print(post_title)
        print(post_img)
        return [data_post]
    
    except Exception as e:
        print("except", e)
        return [{
            'title': '[error] ' + str(e),
            'img' : '',
            'content': '',
            'id': 1,
            'url_post':url_post
        }]


    # print('download {} done!'.format(cat))

    # with(open('{}detik-{}.json'.format(DATA_DIR, cat), 'w')) as fl:
        # json.dump(populer_json, fl)


def load_populer(cat):
    with(open('{}detik-{}.json'.format(DATA_DIR, cat), 'r')) as fl:
        pop_posts = json.load(fl)
    return pop_posts


if __name__ == '__main__':
    if platform.system() == 'Darwin':
        app.run(debug=True)
    else:
        app.run()