#!/usr/bin/python3
# See 'LICENSE' for license details.
import urllib3
import sys
from bs4 import BeautifulSoup
from docopt import docopt

usage_text = """
torrentfinder.py Copyright 2015 Nicholas Parkanyi
Usage: torrentfinder.py [options] <search_terms>...

--help, -h                    Display this usage info.
--number=results, -n results  Number of results to display.
--seeders=min, -s min         Filter results based on minimum number of seeders.
--website=site, -w site       'kt' for kat.cr (default), 'pb' for thepiratebay.la.

"""

args = docopt(usage_text)


class TorrentInfo:
    def __init__(self, name, size, seeders, magnet):
        self.name = name
        self.size = size
        self.seeders = seeders
        self.magnet = magnet

    def print_info(self):
        print(' ' + '_' * len(self.name))
        print('/' + ' ' * len(self.name) + '\\')
        print(' ' + self.name)
        print(' Size: ', self.size, '    Seeders: ', self.seeders)
        print(' Magnet: ', self.magnet)
        print('\\' + '_' * len(self.name) + '/')


class PageData:
    def __init__(self, url, parse_func):
        self.http = urllib3.PoolManager()
        self.request = self.http.request('GET', url)
        self.html = BeautifulSoup(self.request.data, 'lxml')

        parse_func(self)

        self.torrent_list = [TorrentInfo(self.name_elems[i].text,
                                         self.size_elems[i].text,
                                         self.seed_elems[i].text,
                                         self.magnet_elems[i].get('href'))
                             for i in range(len(self.name_elems))]

    def filter_torrents(self, func):
        self.torrent_list = list(filter(func, self.torrent_list))


def KT_parse_elements(page):
    page.name_elems = page.html.find_all('a', attrs={'class': 'cellMainLink'})
    page.size_elems = page.html.find_all('td', attrs={'class': 'nobr center'})
    page.seed_elems = page.html.find_all('td', attrs={'class': 'green center'})
    page.magnet_elems = page.html.find_all('a',
                                           attrs={'title': 'Torrent magnet link'})


def PB_parse_elements(page):
    page.name_elems = page.html.find_all('a', attrs={'class': 'detLink'})
    page.size_elems = page.html.find_all('font', attrs={'class': 'detDesc'})
    seed_elems_tmp = page.html.find_all('td', attrs={'align': 'right'})
    page.magnet_elems = page.html.find_all('a', attrs={'title': 'Download this torrent using magnet'})
    page.seed_elems = []
    for i in range(len(seed_elems_tmp)):
        if i % 2 == 0:
            page.seed_elems.append(seed_elems_tmp[i])


max_results = 4
min_seeders = 0
search_terms = ''

if len(args['<search_terms>']) == 0:
    print(usage_text)
    sys.exit()

if (args['--number']):
    max_results = int(args['--number'])

if (args['--seeders']):
    min_seeders = int(args['--seeders'])

if (args['--help']):
    print(usage_text)
    sys.exit()

for i in range(len(args['<search_terms>'])):
    search_terms = search_terms + args['<search_terms>'][i] + '%20'

if args['--website'] == 'pb':
    page = PageData('https://thepiratebay.la/search/' + search_terms + '/',
                    PB_parse_elements)
else:
    page = PageData('http://kat.cr/usearch/' + search_terms + '/',
                    KT_parse_elements)

page.filter_torrents(lambda x: int(x.seeders) >= min_seeders)

for i in range(min(max_results, len(page.torrent_list))):
    page.torrent_list[i].print_info()
