'''
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
python3 -m pip install Flask
export FLASK_APP=2ch.py; python3 -m flask run --host=0.0.0.0 &
'''

from flask import Flask
import requests

boards = ['news', 'po', 'b']

def get_threads(board): return requests.get(f'https://2ch.hk/{board}/threads.json').json()['threads']

template = '''
<table>
<!-- placeholder -->    
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

app = Flask(__name__)

@app.route('/')
def hello_world():
    threads = []
    for board in boards:
        board_threads = get_threads(board)

        for bt in board_threads:
            bt['board'] = board

        threads += board_threads

    threads_str = ''
    # for thread in sorted(threads, key=lambda x: x['views'], reverse=True):
    for thread in sorted(threads, key=lambda x: x['score'], reverse=True):
        subject      = thread['subject'][:70]
        views        = thread['views']
        score        = round(thread['score'], 1)
        comments     = thread['posts_count']
        board        = thread['board']
        url          = f"https://2ch.hk/{board}/res/{thread['num']}.html"
        threads_str += f'''
            <tr>
            <th><a href='{url}'>{subject}</a></th>
            <th>score {score}</th>
            <th>views {views}</th>
            <th>comments {comments}</th>
            <th>{board}</th>
            </tr>
        '''

    html_str = (
        template
        .replace('<!-- placeholder -->', threads_str)
    )

    # html = pathlib.Path(__file__).parent /'2ch.html'
    # html.write_text(html_str)
    # webbrowser.open(html.resolve().as_uri())

    return html_str
