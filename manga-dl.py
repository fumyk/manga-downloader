#!/usr/bin/env python3
import os

import click
import requests


@click.command()
@click.argument('url', type=str)
@click.option('--skip', default=0, type=int, help='Skip first n chapters')
@click.option('--without-progressbar', is_flag=True)
def main(url, skip, without_progressbar):
    if 'mangaclub.ru' in url:
        from mangaclubru import get_view
        from mangaclubru import parse
        from mangaclubru import FILE_EXTENSION
    else:
        exit('Wrong url')

    main_page_url = get_view(requests.get(url).text)
    for o in parse(requests.get(main_page_url).text, skip, without_progressbar):
        if not os.path.exists(o.get('name') + '/' + o.get('chapter')):
            os.makedirs(o.get('name') + '/' + o.get('chapter'))

        file_path = o.get('name') + '/' + o.get('chapter') + '/' + o.get('page') + FILE_EXTENSION
        response = requests.get(o.get('image'))
        with open(file_path, 'wb') as out:
            out.write(response.content)
        del response
    exit('Completed')


if __name__ == '__main__':
    main()
