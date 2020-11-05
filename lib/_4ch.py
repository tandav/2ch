import requests
import itertools
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
    # subject     = thread.get('sub') or thread.get('com').replace('<br>', ' ') or 'x' * 70
    subject     = thread.get('sub') or thread.get('com') or 'x' * 70
    subject     = util.html2text(subject)
    time_ago    = thread['time_ago']
    posts_count = thread['replies']
    board       = thread['board']
    url         = f"https://boards.4chan.org/{board}/thread/{thread['no']}"
    return util.thread2html(subject, time_ago, posts_count, board, url)


def get_html(boards = ('news', 'pol', 'b')):
    return util.get_html(get_threads, boards, 'time', 'replies', thread2html)
