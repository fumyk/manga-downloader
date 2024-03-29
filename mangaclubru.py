import os

import requests as http
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

ROOT_URL = 'https://mangaclub.ru/'
VIEW_URL = 'https://mangaclub.ru/manga/view/'
FILE_EXTENSION = '.jpg'
DONOTDOWNLOAD = False # debug


def process(url, skip):
    main_page = BeautifulSoup(http.get(url).text, 'html.parser')
    div = main_page.find('div', {'class': 'read_manga'})
    if div.a.get('href') == "javascript:document.write(AdultManga)":
        view_id = div.script.string.split('/view/')[1].split('"')[0]
    else:
        view_id = div.a.get('href').split('/view/')[1]

    soup = BeautifulSoup(http.get(VIEW_URL + view_id).text, 'html.parser')
    name = soup.find('div', {'class': 'head-body container'}).h2.a.string.replace('/', '-')
    chapter_list = soup.find('div', {'class': 'manga-thumbs-chapters scroll-chapters'})
    chapters = []
    for link in chapter_list.find_all('a'):
        chapters.append(link.get('href'))
    if skip > 0:
        print('Skipping first {} chapters'.format(str(skip)))
        chapters = chapters[skip:]

    session = http.Session()
    session.mount(ROOT_URL, HTTPAdapter(max_retries=20))
    # main loop
    for a in chapters:
        soup = BeautifulSoup(session.get(a).text, 'html.parser')
        current_chapter_pages = soup.find('div', {'class': 'manga-lines-page'}).find_all('a')
        chapter_id = current_chapter_pages[0].get('data-c')
        print('Processing chapter', chapter_id)
        current_chapter_path = name + '/' + chapter_id
        if not os.path.exists(current_chapter_path):
            os.makedirs(current_chapter_path)
        for page in current_chapter_pages:
            file_path = current_chapter_path + '/' + page.get('data-p') + FILE_EXTENSION
            if os.path.exists(file_path) or DONOTDOWNLOAD:
                continue
            response = session.get(page.get('data-i'))
            with open(file_path, 'wb') as out:
                out.write(response.content)
            del response
        # update chapter list
        chapter_list = soup.find('div', {'class': 'manga-thumbs-chapters scroll-chapters'})
        for l in chapter_list.find_all('a'):
            tc = l.get('href')
            if tc not in chapters:
                chapters.append(tc)
