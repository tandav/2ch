import requests
import itertools
import collections
import re
from . import util


def viral_comments(thread, top_k=None, min_replies=None):
    json_url = f"https://a.4cdn.org/{thread['board']}/thread/{thread['id']}.json"
    T = util.try_till_success(lambda: requests.get(json_url).json()['posts'], maxtrials=3)
    if not T: return []

    quotes = collections.Counter()

    for t in T:
        if com := t.get('com'):
            q = map(int, set(re.findall(r'(?<=href="#p)\d+(?=" class="quotelink")', com)))
            quotes.update(q)

    t0 = T[0]['no']
    most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
    if t0 in most_quoted:
        del most_quoted[t0]

    for t in T:
        if (count := most_quoted.get(t['no'])) and (com := t.get('com')):
            yield util.html2text(com, newline=False), count


def mapper(thread):
    thread['comment'] = thread.get('com')
    thread['title'] = thread.get('sub') or thread['comment'] or 'x' * 70
    thread['timestamp'] = thread['time']
    thread['dt'] = util.add_ago_to_last_day_threads(thread['timestamp'])
    thread['time_ago'] = util.ago(thread['dt'])
    thread['posts_count'] = thread['replies']
    thread['chan'] = '4ch'
    return thread


def board_threads(board):
    _ = requests.get(f'https://a.4cdn.org/{board}/catalog.json').json()
    _ = (x['threads'] for x in _)
    threads = itertools.chain.from_iterable(_)
    threads = list(threads)
    for thread in threads:
        thread['board'] = board
        id_ = thread['no']
        thread['id'] = id_
        thread['url'] = f"https://boards.4chan.org/{board}/thread/{id_}"
        thread = mapper(thread)
    return threads

boards = 'news', 'pol', 'b', 'sci', 'bant', 'trash'
