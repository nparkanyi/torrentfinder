torrentfinder
=============
Command line tool that searches for torrents online. Requires **python3**, **BeautifulSoup4**, **docopt**,
**lxml**, and **urllib3**. Copyright 2015-2017 Nicholas Parkanyi, see LICENSE.

    Usage: torrentfinder.py [options] <search_terms>...

    --help, -h                    Display this usage info.
    --number=results, -n results  Number of results to display.
    --seeders=min, -s min         Filter results based on minimum number of seeders.
    --website=site, -w site       'pb' for thepiratebay.org(default), '1337x' for 1337x.to.
