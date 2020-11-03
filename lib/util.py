import datetime
import itertools
import operator


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


def add_ago_to_last_day_threads(threads, name):
    now = datetime.datetime.now() 
    for thread in threads:
        ts = datetime.datetime.fromtimestamp(thread[name]) # also try lasthit
        if now - ts > datetime.timedelta(days=1):
            continue
        thread['time_ago'] = ago(now.timestamp() - ts.timestamp())
        yield thread


def thread2html(subject, time_ago, posts_count, board, url):
    return f'''
    <tr>
        <th><a href='{url}'>{subject}</a></th>
        <th>{time_ago}</th>
        <th>posts {posts_count}</th>
        <th>{board}</th>
    </tr>
    '''


def html_table(get_threads, boards, time_key, posts_key, thread2html):
    _ = map(get_threads, boards)
    _ = itertools.chain.from_iterable(_)
    _ = add_ago_to_last_day_threads(_, time_key)
    _ = sorted(_, key = operator.itemgetter(posts_key), reverse = True,)
    _ = map(thread2html, _)
    _ = ''.join(thread for thread in _)
    return _
