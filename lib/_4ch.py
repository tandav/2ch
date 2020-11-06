import requests
import itertools
from . import util


def mapper(thread):
    thread['title'] = thread.get('sub') or thread.get('com') or 'x' * 70
    thread['timestamp'] = thread['time']
    thread['time_ago'] = util.add_ago_to_last_day_threads(thread['timestamp'])
    thread['posts_count'] = thread['replies']
    return thread


def board_threads(board):
    _ = requests.get(f'https://a.4cdn.org/{board}/catalog.json').json()
    _ = (x['threads'] for x in _)
    threads = itertools.chain.from_iterable(_)
    threads = list(threads)
    for thread in threads:
        thread['board'] = board
        thread['url'] = f"https://boards.4chan.org/{board}/thread/{thread['no']}"
        thread = mapper(thread)
    return threads

boards = 'news', 'pol', 'b'
