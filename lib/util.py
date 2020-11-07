import datetime
import itertools
import operator
import string
import re
import html
import time
from . import _4ch, _2ch


def html2text(htm, newline=False):
    ret = html.unescape(htm)
    ret = ret.translate({8209: ord('-'), 8220: ord('"'), 8221: ord('"'), 160: ord(' '),})
    ret = re.sub(r"\s", " ", ret, flags = re.MULTILINE)
    if newline:
        ret = re.sub("<br>|<br />|</p>|</div>|</h\d>", '\n', ret, flags = re.IGNORECASE)
    else:
        ret = re.sub("<br>|<br />|</p>|</div>|</h\d>", ' ', ret, flags = re.IGNORECASE)
    ret = re.sub('<.*?>', ' ', ret, flags=re.DOTALL)
    ret = re.sub(r"  +", " ", ret)
    return ret


def ago(e):
    # e: pass timedelta between timestamps in 1579812524 format
    e *= 1000 # convert to 1579812524000 format
    t = round(e / 1000)
    n = round(t /   60)
    r = round(n /   60)
    o = round(r /   24)
    i = round(o /   30)
    a = round(i /   12)
    if   e <  0: return              'just now'
    elif t < 10: return              'just now'
    elif t < 45: return str(t) + ' seconds ago'
    elif t < 90: return          'a minute ago'
    elif n < 45: return str(n) + ' minutes ago'
    elif n < 90: return           'an hour ago' 
    elif r < 24: return str(r) +   ' hours ago'
    elif r < 36: return             'a day ago'
    elif o < 30: return str(o) +    ' days ago'
    elif o < 45: return           'a month ago'
    elif i < 12: return str(i) +  ' months ago'
    elif i < 18: return            'a year ago'
    else:        return str(a) +   ' years ago'


def add_ago_to_last_day_threads(timestamp):
    return (datetime.datetime.now() - datetime.datetime.fromtimestamp(timestamp)).total_seconds()


def thread2html(thread):
    title = html2text(thread['title'])
    time_ago = thread['time_ago']
    board = thread['board']
    posts_count = thread['posts_count']
    url = thread['url'] 
    return f'''
    <tr>
        <th><a href='{url}' target='_blank'>{title}</a></th>
        <th>{time_ago}</th>
        <th>posts {posts_count}</th>
        <th>{board}</th>
    </tr>
    '''


def make_html(x):
    return string.Template(
    '''
    <table>
    $threads
    </table>

    <style>
    table {
        white-space: nowrap;
        margin: auto;
        background-color: rgba(0, 0, 0, 0.03);
        border-spacing: 30px 0;
    }

    th {
        font-family: Verdana;
        font-size: 9pt;
        font-weight: normal;
        text-align: left;
        max-width: 40vw;
        text-overflow: ellipsis;
        overflow: hidden;
    }

    a { color: black; text-decoration: none; }
    a:visited { color: rgb(200,200,200); }
    a:hover { text-decoration: underline; }
    </style>
    '''
    ).substitute(threads=x)


def boards_threads(board_threads, boards):
    _ = map(board_threads, boards)
    _ = itertools.chain.from_iterable(_)
    return _


def get_html(module, sortby='posts_count'):
    _ = boards_threads(module.board_threads, module.boards)
    _ = sorted(_, key = operator.itemgetter(sortby), reverse = True)
    _ = map(thread2html, _)
    _ = ''.join(thread for thread in _)
    return make_html(_)


def get_threads():
    for trial in itertools.count():
        try:
            threads = list(itertools.chain(
                boards_threads(_4ch.board_threads, _4ch.boards),
                boards_threads(_2ch.board_threads, _2ch.boards),
            ))
        except:
            print(f'bad JSON, trial {trial}, sleep 2 seconds and retry...')
            time.sleep(2)
        else:
            return threads
