import datetime
import itertools
import operator
import string
import re
import html
import time
from . import _4ch, _2ch


def try_till_success(f, maxtrials=None):
    it = itertools.count()
    if maxtrials: it = itertools.islice(it, maxtrials)
    for trial in it:
        try:
            out = f()
        except:
            print(f'{trial} failed, sleep 2 seconds and retry...')
            time.sleep(2)
        else:
            return out


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
    _ = filter(lambda x: x['dt'] < 60 * 60 * 24 * 1.5, _) # last number is days
    # _ = filter(lambda x: x['posts_count'] > 20, _)
    _ = list(_)
    return _


def get_html(module, sortby='posts_count'):
    _ = boards_threads(module.board_threads, module.boards)
    _ = sorted(_, key = operator.itemgetter(sortby), reverse = True)
    _ = map(thread2html, _)
    _ = ''.join(thread for thread in _)
    return make_html(_)


def get_threads():
    threads = try_till_success(lambda: list(itertools.chain(
        boards_threads(_4ch.board_threads, _4ch.boards),
        boards_threads(_2ch.board_threads, _2ch.boards),
    )))
    return threads or []
    # for trial in itertools.count():
    #     try:
    #         threads = list(itertools.chain(
    #             boards_threads(_4ch.board_threads, _4ch.boards),
    #             boards_threads(_2ch.board_threads, _2ch.boards),
    #         ))
    #     except:
    #         print(f'bad JSON, trial {trial}, sleep 2 seconds and retry...')
    #         time.sleep(2)
    #     else:
    #         return threads


def color(v):
    if   v <   5: c = 236
    elif v <  10: c = 237
    elif v <  15: c = 238
    elif v <  20: c = 239
    elif v <  25: c = 240
    elif v <  30: c = 241
    elif v <  35: c = 242
    elif v <  40: c = 243
    elif v <  45: c = 244
    elif v <  50: c = 245
    elif v <  55: c = 246
    elif v <  60: c = 247
    elif v <  65: c = 248
    elif v <  70: c = 249
    elif v <  75: c = 250
    elif v <  80: c = 251
    elif v <  85: c = 252
    elif v <  90: c = 253
    elif v <  95: c = 254
    elif v < 100: c = 255
    elif v < 200: c = 82  # green
    elif v < 300: c = 87  # blue
    elif v < 400: c = 226 # yellow
    elif v < 500: c = 208 # orange
    elif v>= 500: c = 196 # red
    return c