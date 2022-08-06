import json
import os
import time
from scholarly import scholarly
from configparser import ConfigParser
from datetime import datetime, timedelta


class SearchEngine():
    def __init__(self):
        pass

    def search(self, val, method):
        if method == 'id':
            return self.searchByID(val)

    def searchByID(self, user_id):
        result = scholarly.search_author_id(user_id)
        return result

    def searchByPub(self, pub):
        pass


# To be upgraded to Database
class Citation():
    def __init__(self, path):
        self.path = path
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
        if not os.path.isfile(self.path):
            self.write({})

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        return d

    def write(self, d):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(d, f)

    def update(self, author_id, author_name, citation):
        d = self.read()
        if author_id not in d:
            d[author_id] = {'name':author_name}
        d[author_id][self.today] = citation
        self.write(d)

    def compare(self, author_id):
        d = self.read()
        today_citation = d[author_id][self.today]
        try:
            yesterday_citation = d[author_id][self.yesterday]
        except:
            yesterday_citation = 0
        d[author_id]['increase'] = today_citation - yesterday_citation
        self.write(d)
        
        return (today_citation, yesterday_citation)

    # return today's citation and the incrase for presentation
    def present(self):
        d_present = {}
        d_all = self.read()
        for author_id in d_all:
            author_name = d_all[author_id]['name']
            if author_name not in d_present:
                d_present[author_name] = {'citation':d_all[author_id][self.today], 'increase':d_all[author_id]['increase']}
        return d_present


def checkUpdate(searcher, citation, conf, single_author=None, force=False):
    today = time.localtime()[0:3]
    last_modified = time.localtime(os.stat(citation.path).st_mtime)[0:3]
    if today != last_modified or force == True:
        if single_author != None:
            author_id = conf['Authors'][single_author]
            result = searcher.search(author_id, method='id')
            citation.update(author_id, result['name'], result['citedby'])
            today_citation, yesterday_citation = citation.compare(author_id)
            print('%s today citation: %d, yesterday citation: %d, %d ⬆'%(result['name'], today_citation, yesterday_citation, (today_citation-yesterday_citation)))
        else:
            for author_label in conf['Authors']:
                author_id = conf['Authors'][author_label]
                result = searcher.search(author_id, method='id')
                citation.update(author_id, result['name'], result['citedby'])
                today_citation, yesterday_citation = citation.compare(author_id)
                print('%s today citation: %d, yesterday citation: %d, %d ⬆'%(result['name'], today_citation, yesterday_citation, (today_citation-yesterday_citation)))


if __name__ == '__main__':
    conf = ConfigParser()
    conf.read("config.ini", encoding='utf-8')
    Proxy = conf['Proxy']
    Authors = conf['Authors']
    Settings = conf['Settings']

    os.environ["http_proxy"] = Proxy['http_proxy']
    os.environ["https_proxy"] = conf['Proxy']['https_proxy']

    searcher = SearchEngine()
    citation = Citation(Settings['db_path'])
    checkUpdate(searcher, citation, conf, force=True)
    print(json.dumps(citation.read(), indent=4))
    