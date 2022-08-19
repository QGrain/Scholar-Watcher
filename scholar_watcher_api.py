import json
import os
import time
from scholarly import scholarly
from configparser import ConfigParser
from datetime import datetime, timedelta, date
import requests
from bs4 import BeautifulSoup
import threading


g_timer_flag = 1


class TimerManager():
    def __init__(self, thread_handler): 
        self.timer_handler = thread_handler

    def __del__(self): 
        global g_timer_flag
        g_timer_flag = 0
        print("Main thread exit, Timer should cancel as well", g_timer_flag)
        self.timer_handler.cancel()


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

    def fetchRecentTopKPub(self, user_id, top_k):
        # notice! This can only fetch the top k pubs ranked by citations not pub-time.
        # Now it is deprecated. Use fetchLatestKPub() instead!
        this_year_str = str(datetime.now().year)
        result = self.searchByID(user_id)
        author = scholarly.fill(result)

        ret_pubs = {}
        cnt = 0
        for pub in author['publications']:
            if cnt >= top_k:
                break
            if 'pub_year' in pub['bib'] and str(pub['bib']['pub_year']) == this_year_str:
                ret_pubs[pub['bib']['title']] = {'pub_year': str(pub['bib']['pub_year']), 'num_citations': str(pub['num_citations'])}
                cnt += 1
        return ret_pubs


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

    def getSequence(self, author_ids):
        d_all = self.read()
        seq = []
        for author_id in author_ids:
            citation_lines = []
            for key in sorted(d_all[author_id]):
                if '-' in key and key != 'increase' and key != 'name':
                    # print(d_all[author_id][key])
                    citation_lines.append(int(d_all[author_id][key]))
            seq.append(citation_lines)
        # print(seq)
        return seq

    def copyOneDay(self, date):
        pass
        # If yesterday is blank, then recursively copy the day before yesterday


def getPlotData(d_all, author_ids):
    data = []
    first_ptime, earliest_date = 1, datetime(2200, 1, 1)
    for author_id in author_ids:
        plot_data = {'X_DATA':[], 'Y_DATA':[]}
        for key in sorted(d_all[author_id]):
            if '-' in key and key != 'increase' and key != 'name':
                plot_data['Y_DATA'].append(int(d_all[author_id][key]))
                ptime = time.strptime(key, '%Y-%m-%d')
                plot_data['X_DATA'].append(datetime(ptime[0], ptime[1], ptime[2]))
                if first_ptime == 1:
                    earliest_date = ptime
                    first_ptime = 0
                if ptime < earliest_date:
                    earliest_date = ptime
        data.append(plot_data)
    
    for i in range(len(data)):
        for j in range(len(data[i]['X_DATA'])):
            data[i]['X_DATA'][j] = (data[i]['X_DATA'][j] - earliest_date).days
    return (data, earliest_date)


def checkUpdate(searcher, citation, conf, single_author=None, force=False):
    today = time.localtime()[0:3]
    today_str = datetime.now().strftime('%Y-%m-%d')
    # last_modified = time.localtime(os.stat(citation.path).st_mtime)[0:3] # bug, sholdn't rely on the modify time. should fetch from json
    d_all = citation.read()
    first_author = conf.options('Authors')[0]
    if today_str not in d_all[conf['Authors'][first_author]] or force == True:
    # if today != last_modified or force == True:
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



def fetchLatestKPub(user_id, latest_k):
    head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    url = 'https://scholar.google.com.hk/citations?user=' + user_id + '&view_op=list_works&sortby=pubdate'
    r = requests.get(url, headers=head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    recent_pubs = soup.find_all(class_='gsc_a_tr')
    k = min(20, latest_k)

    latest_pubs = {}
    for i in range(k):
        title = recent_pubs[i].contents[0].contents[0].string
        pub_year = recent_pubs[i].contents[0].contents[2].contents[1].string.split(',')[-1]
        num_citations = recent_pubs[i].contents[1].string
        if num_citations == None:
            num_citations = 0
        latest_pubs[title] = {'pub_year': pub_year, 'num_citations': num_citations}
    return latest_pubs


def autoUpdateEveryDay(searcher, citation, conf):
    global g_timer_flag
    if g_timer_flag != 0:
        print('auto checkUpdate() once a day')
        checkUpdate(searcher, citation, conf, single_author=None, force=True)
        # timer = threading.Timer(86400, autoUpdateEveryDay, (searcher, citation, conf))
        # timer.start()


# todo: solve child thread exit problem. or it would wait for a hole day.
def getSecondsToTime(hour, minute, second):
    now = datetime.now()
    target_time = datetime(now.year, now.month, now.day, hour, minute, second)
    tomorrow_target_time = target_time + timedelta(days=1)
    if now.hour <= hour and now.minute <= minute and now.second <= second:
        rest_seconds = (target_time - now).seconds
    else:
        rest_seconds = (tomorrow_target_time - now).seconds
    return rest_seconds
    


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
    