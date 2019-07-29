'''
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
python3 -m pip install Flask
export FLASK_APP=2ch.py; python3 -m flask run --host=0.0.0.0 &
'''

from flask import Flask
import requests
import string
import itertools
import operator

boards = ['news', 'po', 'b']

def get_threads(board):
    board_threads = requests.get(f'https://2ch.hk/{board}/threads.json').json()['threads']
    for thread in board_threads:
        thread['board'] = board # add board label
    return board_threads

def thread2html(thread):
    subject      = thread['subject'][:70]
    views        = thread['views']
    score        = round(thread['score'], 1)
    comments     = thread['posts_count']
    board        = thread['board']
    url          = f"https://2ch.hk/{board}/res/{thread['num']}.html"
    return f'''
    <tr>
        <th><a href='{url}'>{subject}</a></th>
        <th>score {score}</th>
        <th>views {views}</th>
        <th>comments {comments}</th>
        <th>{board}</th>
    </tr>
    '''

app = Flask(__name__)

@app.route('/')
def hello_world():
    _ = map(get_threads, boards)
    _ = itertools.chain.from_iterable(_)
    _ = sorted(_, key = operator.itemgetter('score'), reverse = True,)
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
