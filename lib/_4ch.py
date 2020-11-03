import requests
import string
import itertools
import html
from . import util


def get_threads(board):
    _ = requests.get(f'https://a.4cdn.org/{board}/catalog.json').json()
    _ = (x['threads'] for x in _)
    threads = itertools.chain.from_iterable(_)
    threads = list(threads)
    for thread in threads:
        thread['board'] = board
    return threads


def thread2html(thread):
    # subject     = html.unescape(thread['com']).replace('\n', ' ')[:70]
    subject     = thread['com'].replace('<br>', ' ')[:70]
    time_ago    = thread['time_ago']
    posts_count = thread['replies']
    board       = thread['board']
    url         = f"https://boards.4chan.org/{board}/thread/{thread['no']}"
    return util.thread2html(subject, time_ago, posts_count, board, url)


def get_html(boards = ('news', 'po', 'b')):
    return util.get_html(get_threads, boards, 'time', 'replies', thread2html)
