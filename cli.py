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


def color_i(s, i):
    return f"\x1b[38;5;{i}m{s}\033[0m"


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
            color.WHITE(f"{posts_count:>4}"),
            thread['time_ago'],
            color.CYAN(f'{sleep_time} sleep'),
            thread['url'],
        )
        # title_color = color.GREEN if posts_count >= 100 else color.WHITE
        if   posts_count <   5: title_color = 236
        elif posts_count <  10: title_color = 237
        elif posts_count <  15: title_color = 238
        elif posts_count <  20: title_color = 239
        elif posts_count <  25: title_color = 240
        elif posts_count <  30: title_color = 241
        elif posts_count <  35: title_color = 242
        elif posts_count <  40: title_color = 243
        elif posts_count <  45: title_color = 244
        elif posts_count <  50: title_color = 245
        elif posts_count <  55: title_color = 246
        elif posts_count <  60: title_color = 247
        elif posts_count <  65: title_color = 248
        elif posts_count <  70: title_color = 249
        elif posts_count <  75: title_color = 250
        elif posts_count <  80: title_color = 251
        elif posts_count <  85: title_color = 252
        elif posts_count <  90: title_color = 253
        elif posts_count <  95: title_color = 254
        elif posts_count < 100: title_color = 255
        elif posts_count < 300: title_color = 82  # green
        elif posts_count < 500: title_color = 226 # yellow
        elif posts_count>= 500: title_color = 196 # red
        print(color_i(title, title_color))
        # print(color.GREEN('=' * 72), color.WHITE(thread['time_ago']))
        print(color_i('─'*100, 236))
        time.sleep(sleep_time)

# s = 7777777777777777777777
# for i in range(87, 81, -1):
# for i in range(256):
#     print(color_i(i, i))
    # print(f"\x1b[38;5;{i}m {i}")
    # print(f'\033[87m{s}\033[0m')