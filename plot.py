'''
TODO:
upper left corner:
top 10 titles with highest derivative (just difference: curr - prev count) (maybe take lag=5 instead of lag=1), maybe take last 5 minutes/ 10 minutes
    better: print text with plot line (add padding)
    make em bold (plot lines)
    blog post
    tj post
    telegram bot
exception, timeout, retry
gcp lambda
get a name : current name 2ch-observer
clickable links (html)
websockets? realtime update?
alpha = k * avg diff
'''


import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from json.decoder import JSONDecodeError

import pandas as pd
import datetime
from pathlib import Path
import time
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import dateutil

from lib import util, _4ch, _2ch
import itertools

def requests_retry_session(
    retries=10,
    backoff_factor=0.3,
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


rrs = requests_retry_session()


DB_PATH  = Path('db.pkl')
MSK = dateutil.tz.gettz('Europe/Moscow')
DATE_FORMAT = DateFormatter('%H:%M', tz=MSK)
YLIM = 20 # stddev
MIN_POSTS = 25
TOP_RISING = 40
TOP_RISING_LAG = 5 # todo time lag instead of index lag
SLEEP_TIME = 0.2 # sleep time between requests

# def try_get_json(url):
#     r = rrs.get(url)
#     try:
#         return r.json()
#     except JSONDecodeError:
#         print(f'bad JSON at {url}')
#
# def board_info(board):
#     info = dict()
#
#     # index = rrs.get().json()
#     index = try_get_json(f'https://2ch.hk/{board}/index.json')
#     if index is None:
#         return dict()
#
#     info.update(threads_2_info(index['threads']))
#     for page in index['pages'][1:-1]:
#         time.sleep(SLEEP_TIME)
#         page_threads = rrs.get(f'https://2ch.hk/{board}/{page}.json').json()['threads']
#         info.update(threads_2_info(page_threads))
#     return info


# def get_info(boards=('news', 'po', 'b')):
#     info = dict()
#     for board in boards:
#         info.update(board_info(board))
#     return info

def get_info():
    threads = itertools.chain(
        util.boards_threads(_4ch.board_threads, _4ch.boards),
        util.boards_threads(_2ch.board_threads, _2ch.boards),
    )

    info = dict()
    for thread in threads:
        info[thread['id']] = thread['posts_count'], util.html2text(thread['title'])
    return info

if not DB_PATH.exists():
    pd.DataFrame().to_pickle(DB_PATH)

while True:
    # breakpoint()
    d = pd.read_pickle(DB_PATH)#.tail(1000)

    if d.shape[0]:
        d = d[d.index > datetime.datetime.now(tz=MSK) - datetime.timedelta(days=1)]
        last_row = d.iloc[-1]
        d = d.drop(columns=last_row[last_row.isna()].index)

    now = datetime.datetime.now(tz=MSK)

    info = get_info()

    for thread, (count, title) in info.items():
        if count < MIN_POSTS:
            continue
        d.loc[now, thread] = count

    print(now, d.shape)
    d.astype('float32').to_pickle(DB_PATH)

    diff = d.loc[(now - d.index).seconds < 60 * 60 * 1.5].diff().mean()
    # diff = d.iloc[-TOP_RISING_LAG - 1:].diff().mean()
    mean = d.mean(axis=1)
    std  = d.std(axis=1)

    # mean_global = d.mean().mean()
    # std_global  = d.std().mean()
    # max_global  = d.max().max()
    # min_global  = d.min().min()

    # y_low  = max(mean_global - YLIM * std_global, min_global)
    # y_high = min(mean_global + YLIM * std_global, max_global)

    # ax = d.interpolate(limit_area='inside').plot(figsize=(16, 10), legend=False, marker=None, linestyle='-', linewidth=0.9)
    # ax = d.plot(figsize=(18, 10), legend=False, marker=None, markersize=1, linestyle='-', linewidth=0.9)
    plt.figure(figsize=(18, 10))
    for alpha, (c, s) in zip(diff, d.items()):
        ax = s.plot(alpha=alpha)
    ax.xaxis.set_major_formatter(DATE_FORMAT)
    # ax.yaxis.set_major_formatter(PRICE_FORMAT)
    mean.plot(color='black', marker=None, linestyle='-', linewidth=3)
    plt.fill_between(std.index, mean - std, mean + std, color='grey', alpha=.1, zorder=-1)

    plt.grid(lw=0.3)
    plt.title(f'2ch.hk threads, MIN_POSTS={MIN_POSTS} TOP_RISING={TOP_RISING}, TOP_RISING_LAG={TOP_RISING_LAG}')
    plt.xlabel(f'last update:    {now:%Y %b %d %H:%M:%S} MSK')
    plt.ylabel('comments')
    # top_rising = d.iloc[[-TOP_RISING_LAG - 1, -1]].diff().iloc[-1].nlargest(TOP_RISING)
    top_rising = diff[diff.index.isin(info)].nlargest(TOP_RISING)

    t_end = d.index[-1]

    for i, (thread, delta) in enumerate(top_rising.items(), 1):
        count, title = info[thread]
        # count = i * 100
        # title = f'TOP {i}: Коронавирус / COVID-19 № 719 ОПЕРАТИВНЫЙ ШТАБ УРОВНЯ /PO/'
        plt.text(
            x = t_end,
            y = count,
            s = f'#{i:>2} {title[:70]}',
            horizontalalignment='left',
            verticalalignment='center',
            #         family = 'SF Mono',
            fontsize = 6,
            #         color = font_color,
        )
    if d.shape[0] > TOP_RISING_LAG:
        # (now - d.index).seconds < 60 * 60 * 1.5
        plt.axvline(d.index[(now - d.index).seconds < 60 * 60 * 1.5][0], linestyle='--', color='black')
        # plt.axvline(d.index[-TOP_RISING_LAG - 1], linestyle='--', color='black')
    plt.ylim(bottom=MIN_POSTS)
    plt.tight_layout()

    ax.figure.savefig('threads.png')
    fig = ax.get_figure()
    plt.close(fig)

    # time.sleep(55)
    time.sleep(5)
