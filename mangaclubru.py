import progressbar
import requests as http
from bs4 import BeautifulSoup

VIEW_URL = 'https://mangaclub.ru/manga/view/'
FILE_EXTENSION = '.jpg'


def get_view(page):
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', {'class': 'read_manga'})
    if div.a.get('href') == 'javascript:document.write(AdultManga)':
        view_id = div.script.string.split('/view/')[1].split('"')[0]
    else:
        view_id = div.a.get('href').split('/view/')[1]
    return VIEW_URL + view_id


def parse(page, skip):
    """
    Returns image link generator
    """
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.find('div', {'class': 'head-body container'}).h2.a.string.replace('/', '-')
    print('Getting chapter list for ' + name)
    chapter_list = soup.find('div', {'class': 'manga-thumbs-chapters scroll-chapters'})
    chapters = []
    for link in chapter_list.find_all('a'):
        chapters.append(link.get('href'))
    c = len(chapters)
    print('Found {} chapters\nDownloading...'.format(str(c)))
    if skip > 0:
        print('Skipping first {} chapters'.format(str(skip)))
    chapters = chapters[skip:]
    # main loop
    n = 1 + skip
    bar = progressbar.ProgressBar(max_value=c, widgets=[progressbar.SimpleProgress(), progressbar.Bar()])
    for a in chapters:
        bar.update(n)
        soup = BeautifulSoup(http.get(a).text, 'html.parser')
        for manga_link in soup.find('div', {'class': 'manga-lines-pages'}).find_all('a'):
            yield {'name': name,
                   'chapter': manga_link.get('data-c'),
                   'page': manga_link.get('data-p'),
                   'image': manga_link.get('data-i')}
        n += 1
