import requests
import itertools
from . import util


def mapper(thread):
    thread['title'] = thread.get('sub') or thread.get('com') or 'x' * 70
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

boards = 'news', 'pol', 'b'
