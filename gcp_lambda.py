# def hello_world(request):
#     """Responds to any HTTP request.
#     Args:
#         request (flask.Request): HTTP request object.
#     Returns:
#         The response text or any set of values that can be turned into a
#         Response object using
#         `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
#     """
#     request_json = request.get_json()
#     if request.args and 'message' in request.args:
#         return request.args.get('message')
#     elif request_json and 'message' in request_json:
#         return request_json['message']
#     else:
#         return f'Hello World!'

import requests
import string
import itertools
import operator
import datetime


boards = ['news', 'po', 'b']


def ago(e):
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

def get_threads(board):
    board_threads = requests.get(f'https://2ch.hk/{board}/threads.json').json()['threads']
    for thread in board_threads:
        thread['board'] = board # add board label
    return board_threads

def thread2html(thread):
    subject     = thread['subject'][:70]
    time_ago    = thread['time_ago']
    posts_count = thread['posts_count']
    board       = thread['board']
    url         = f"https://2ch.hk/{board}/res/{thread['num']}.html"
    return f'''
    <tr>
        <th><a href='{url}'>{subject}</a></th>
        <th>{time_ago}</th>
        <th>posts {posts_count}</th>
        <th>{board}</th>
    </tr>
    '''

def add_ago_to_last_day_threads(threads):
    out = []
    for thread in threads:
        now = datetime.datetime.now() 
        ts = datetime.datetime.fromtimestamp(thread['timestamp']) # also try lasthit
        if now - ts > datetime.timedelta(days=1):
            continue
        thread['time_ago'] = ago(now.timestamp() - ts.timestamp())
        out.append(thread)
    return out

def hello_world(request):
    _ = map(get_threads, boards)
    _ = itertools.chain.from_iterable(_)
    _ = add_ago_to_last_day_threads(_)
    _ = sorted(_, key = operator.itemgetter('posts_count'), reverse = True,)
    _ = map(thread2html, _)
    _ = ''.join(thread for thread in _)
    _ = string.Template(
    '''
    <table>
    $threads
    </table>

    <style>
    table {
        margin: 0px 150px 0px 150px;
        background-color: rgba(0, 0, 0, 0.03);
    }

    th {
        font-family: Verdana;
        font-size: 9pt;
        font-weight: normal;
        text-align: left;
    }

    a { color: black; text-decoration: none; }
    a:visited { color: rgb(200,200,200); }
    a:hover { text-decoration: underline; }
    </style>
    '''
    ).substitute(threads=_)

    return _
