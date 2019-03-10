#return the magnet link element from a 1337x.pl result page
def l337_sub_page(page, sub_url):
    sub_req = page.http.request('GET', sub_url)
    sub_html = BeautifulSoup(sub_req.data, 'lxml')
    return sub_html.find_all('a', attrs={'class': 'btn-acaebece'})[0].get('href')
 
def l337_parse_elements(page):
    page.size_elems = list(map(lambda x: x.text[:x.text.find('B') + 1],
                              page.html.find_all('td', class_ = 'coll-4')))
    page.seed_elems = list(map(lambda x: x.text,
                              page.html.find_all('td', class_ = 'coll-2')))
    page.name_elems = page.html.find_all('td', class_ = 'coll-1')
    page.name_elems = list(map(lambda x: x.find_all('a')[1], page.name_elems))
    sub_urls = list(map(lambda x: x.get('href'), page.name_elems))
    page.name_elems = list(map(lambda x: x.text, page.name_elems))
    page.magnet_elems = list(map(lambda x: l337_sub_page(page, 'https://1337x.to' + x),
                             sub_urls))
 
add_plugin (Plugin('1337x', lambda x: PageData('https://1337x.to/search/'+x+'/1/',
                                                    l337_parse_elements)) )
