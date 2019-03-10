def PB_parse_elements(page):
    page.name_elems = list(map(lambda x: x.text,
                           page.html.find_all('a', attrs={'class': 'detLink'})))
    page.size_elems = list(map(lambda x: x.text[x.text.find('Size') + 7:],
                           page.html.find_all('font', attrs={'class': 'detDesc'})))
    page.size_elems = list(map(lambda x: x[:x.find(',')], page.size_elems))
    seed_elems_tmp = list(map(lambda x: x.text,
                           page.html.find_all('td', attrs={'align': 'right'})))
    page.magnet_elems = list(map(lambda x: x.get('href'),
                           page.html.find_all('a', attrs={'title': 'Download this torrent using magnet'})))
    page.seed_elems = []
    for i in range(len(seed_elems_tmp)):
        if i % 2 == 0:
            page.seed_elems.append(seed_elems_tmp[i])


add_plugin( Plugin('pb', lambda x: PageData('https://thepiratebay.org/search/'+x+'/',
                                            PB_parse_elements)) )
