#!/usr/bin/python3
# See 'LICENSE' for license details.
import urllib3
import sys
import os
from bs4 import BeautifulSoup
from docopt import docopt

usage_text = """
torrentfinder.py Copyright 2015-2017 Nicholas Parkanyi
Usage: torrentfinder.py [options] <search_terms>...

--help, -h                    Display this usage info.
--number=results, -n results  Number of results to display.
--seeders=min, -s min         Filter results based on minimum number of seeders.
--website=site, -w site       'pb' for thepiratebay.org(default), '1337x' for 1337x.to.

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

        self.torrent_list = [TorrentInfo(self.name_elems[i],
                                         self.size_elems[i],
                                         self.seed_elems[i],
                                         self.magnet_elems[i])
                             for i in range(len(self.name_elems))]

    def filter_torrents(self, func):
        self.torrent_list = list(filter(func, self.torrent_list))


class Plugin:
    def __init__(self, name, parse_fun):
        self.name = name
        #parse_fun(search_query) -> PageData, where search_query is sanitized query string
        self.parse_fun = parse_fun

plugins_list = []

def add_plugin(plugin):
    plugins_list.append(plugin)


#load all plugins from the plugins dir
for f in os.listdir('./plugins'):
    exec(open('./plugins/' + f).read())

  

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
    
#remove trailing '%20', fucks up search urls
search_terms = search_terms[:-3]



for plugin in plugins_list:
    print(plugin.name)
    if plugin.name == args['--website']:
        page = plugin.parse_fun(search_terms)

page.filter_torrents(lambda x: int(x.seeders) >= min_seeders)

for i in range(min(max_results, len(page.torrent_list))):
    page.torrent_list[i].print_info()
