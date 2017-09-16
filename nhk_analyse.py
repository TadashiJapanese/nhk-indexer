#!/usr/bin/env python3

import requests, sqlite3, analyse, time, sys, json
from bs4 import BeautifulSoup

NEWS_JSON_ENDPOINT = "http://www3.nhk.or.jp/news/easy/news-list.json"

def remove_already_seen_links(links):
    out = set(links)
    conn = sqlite3.connect('nhk_stats.db')
    c = conn.cursor()
    known = set([row[0] for row in c.execute("select url from nhk_stats")])
    conn.close()
    return links - known

def parse_api_json(data):
    links = set()
    lnk = lambda lId: "http://www3.nhk.or.jp/news/easy/%s/%s.html" % (lId, lId)
    for partition in data:
        for day in partition:
            for story in partition[day]:
                links.add(lnk(story["news_id"]))
    return links

def get_nhk_stories_from_web(endpoint=NEWS_JSON_ENDPOINT):
    data = requests.get(endpoint).json()
    return parse_api_json(data)

def get_nhk_stories_from_file(filename):
    data = json.loads(open(filename, "r").read())
    return parse_api_json(data)

def scrape_story_from_url(url):
    data = requests.get(url).content
    soup = BeautifulSoup(data, "html.parser")
    text = soup.find(id="newsarticle").get_text() 
    return text

def store_stats_in_sqlite(url, stats):
    conn = sqlite3.connect('nhk_stats.db')
    c = conn.cursor()
    for k, v in dick.items():
        c.execute("insert into nhk_stats values (?, ?, ?)", (url, k, v))

    conn.commit()
    conn.close()

    
if __name__ == "__main__":

    links = set()

    if len(sys.argv) == 1:
        links = get_nhk_stories_from_web()
    elif len(sys.argv) == 2:
        links = get_nhk_stories_from_file(sys.argv[1])
    
    newlinks = remove_already_seen_links(links)

    print("links found: %s, ignored: %s" % (len(links), len(links)-len(newlinks)))
    
    for link in newlinks:
        text = scrape_story_from_url(link)
        dick = analyse.for_all_levels_dict(text, 60)    
        store_stats_in_sqlite(link, dick)
        time.sleep(5)
        print("fetched %s" % link)
