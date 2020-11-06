import time
import random
import itertools
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


while True:
    threads = itertools.chain(
        util.boards_threads(_4ch.board_threads, _4ch.boards),
        util.boards_threads(_2ch.board_threads, _2ch.boards),
    )

    threads = filter(lambda thread: thread['dt'] < 60 * 60 * 1.5, threads)
    threads = list(threads)
    random.shuffle(threads)


    for i, thread in enumerate(threads):
        title = thread['title']
        title = util.html2text(title, newline=True)
        posts_count = thread['posts_count']
        sleep_time = round(-12 * 0.7 ** (0.03 * posts_count) + 12, 1)

        print(
            color.YELLOW(f'{i}..{len(threads)}'),
            color.BLUE(thread['board']),
            f"{posts_count:>4}",
            thread['time_ago'],
            color.CYAN(f'{sleep_time} sleep'),
            thread['url'],
        )
        title_color = color.GREEN if posts_count >= 100 else color.WHITE
        print(title_color(title))
        # print(color.GREEN('=' * 72), color.WHITE(thread['time_ago']))
        # time.sleep(0.7)
        print('─'*100)
        time.sleep(sleep_time)
