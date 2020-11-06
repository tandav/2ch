import requests
import string
import itertools
import operator
import html
from . import util


def mapper(thread):
    thread['title'] = thread['subject']
    # title = html.escape(title)
    # title       = util.html2text(title)
    # thread['title'] = thread['comment']#[:100]
    thread['dt'] = util.add_ago_to_last_day_threads(thread['timestamp'])
    thread['time_ago'] = util.ago(thread['dt'])
    return thread


def board_threads(board):
    threads = requests.get(f'https://2ch.hk/{board}/catalog.json').json()['threads']
    for thread in threads:
        thread['board'] = board
        thread['url'] = f"https://2ch.hk/{board}/res/{thread['num']}.html"
        thread = mapper(thread)
    return threads


boards = 'news', 'po', 'b'
