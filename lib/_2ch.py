import requests
import string
import itertools
import operator
import html
import collections
import re
from . import util


def viral_comments(thread, top_k=None, min_replies=None):
    json_url = f"https://2ch.hk/{thread['board']}/res/{thread['id']}.json"
    T = util.try_till_success(lambda: requests.get(json_url).json()['threads'][0]['posts'], maxtrials=3)
    if not T: return []

    quotes = collections.Counter()

    for t in T:
        com = t['comment']
        q = map(int, set(re.findall(r'(?<=#)\d+(?=" class="post-reply-link")', com)))
        quotes.update(q)

    t0 = T[0]['num']
    most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
    if t0 in most_quoted:
        del most_quoted[t0]

    for t in T:
        if count := most_quoted.get(t['num']):
            yield util.html2text(t['comment'], newline=False), count

def mapper(thread):
    # thread['comment'] =
    thread['title'] = thread['subject']
    # title = html.escape(title)
    # title       = util.html2text(title)
    # thread['title'] = thread['comment']#[:100]
    thread['dt'] = util.add_ago_to_last_day_threads(thread['timestamp'])
    thread['time_ago'] = util.ago(thread['dt'])
    thread['chan'] = '2ch'
    return thread


def board_threads(board):
    threads = requests.get(f'https://2ch.hk/{board}/catalog.json').json()['threads']
    for thread in threads:
        thread['board'] = board
        id_ = thread['num']
        thread['id'] = id_
        thread['url'] = f"https://2ch.hk/{board}/res/{id_}.html"
        thread = mapper(thread)
    return threads


boards = 'news', 'po', 'b'
