import time
import random
import itertools
import difflib
from lib import util, _4ch, _2ch


class color:
    BLACK     = lambda s: '\033[30m' + str(s) + '\033[0m'
    RED       = lambda s: '\033[31m' + str(s) + '\033[0m'
    GREEN     = lambda s: '\033[32m' + str(s) + '\033[0m'
    YELLOW    = lambda s: '\033[33m' + str(s) + '\033[0m'
    BLUE      = lambda s: '\033[34m' + str(s) + '\033[0m'
    MAGENTA   = lambda s: '\033[35m' + str(s) + '\033[0m'
    CYAN      = lambda s: '\033[36m' + str(s) + '\033[0m'
    WHITE     = lambda s: '\033[37m' + str(s) + '\033[0m'
    UNDERLINE = lambda s: '\033[4m'  + str(s) + '\033[0m'


def color_i(s, i):
    return f"\x1b[38;5;{i}m{s}\033[0m"


while True:
    threads = util.get_threads()
    threads = filter(lambda thread: thread['dt'] < 60 * 60 * 1.5, threads)
    threads = list(threads)
    random.shuffle(threads)


    for i, thread in enumerate(threads, start=1):
        title = thread['title']
        title = util.html2text(title, newline=True)
        posts_count = thread['posts_count']
        sleep_time = round(-12 * 0.7 ** (0.03 * posts_count) + 12, 1)

        title_color = util.color(posts_count)
        derivative = int(posts_count/thread['dt'] * 1000)


        print('{:<14} {:<10} {} {:>10} {:>18} {:>10} {}'.format(
            color.YELLOW(f'{i}..{len(threads)}'),
            color.BLUE(thread['board']),
            posts_count and f'⬆ {derivative}' or '',
            color.WHITE(f"{posts_count:>4} comments"),
            thread['time_ago'],
            color.CYAN(f'{sleep_time} sleep'),
            thread['url'],
        ))


        if comment := thread.get('comment'):
            comment = util.html2text(comment, newline=True)

            nospace_title   = [c for c in title   if not c.isspace()]
            nospace_comment = [c for c in comment if not c.isspace()]
            min_len = min(len(nospace_title), len(nospace_comment))

            ratio = difflib.SequenceMatcher(lambda x: x.isspace(), nospace_title[:min_len], nospace_comment[:min_len]).ratio()

            if ratio < 0.7:
                print(color_i(title, title_color))
            print(color_i(comment[:500], title_color))
        else:
            print(color_i(title, title_color))

        t0 = time.time()
        for viral_comment, count in {'4ch': _4ch, '2ch': _2ch}[thread['chan']].viral_comments(thread, 3, min_replies=5):
            print(color.WHITE(f'[{count} replies]'), end=' ')
            print(color_i(viral_comment, title_color))

        print(color_i('─'*100, 236))
        time.sleep(max(sleep_time - (time.time() - t0), 0))
