#!/usr/bin/env python3
import click


@click.command()
@click.argument('url', type=str)
@click.option('--skip', default=0, type=int, help='Skip first n chapters')
def main(url, skip):
    if 'mangaclub.ru' in url:
        from mangaclubru import process
    else:
        exit('Wrong url')

    process(url, skip)
    exit('Done')


if __name__ == '__main__':
    main()
