import requests
import string
import itertools
import operator
from . import util


def get_threads(board):
    board_threads = requests.get(f'https://2ch.hk/{board}/catalog.json').json()['threads']
    for thread in board_threads:
        thread['board'] = board # add board label
    return board_threads


def thread2html(thread):
    subject     = thread['subject'][:70]
    time_ago    = thread['time_ago']
    posts_count = thread['posts_count']
    board       = thread['board']
    url         = f"https://2ch.hk/{board}/res/{thread['num']}.html"
    return util.thread2html(subject, time_ago, posts_count, board, url)
    

def html_table(boards = ('news', 'po', 'b')):
    return util.html_table(get_threads, boards, 'timestamp', 'posts_count', thread2html)
