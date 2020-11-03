'''
https://2ch.hk/api
TODO: githooks (git push github, git push prod) / or git hooks on github
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
python3 -m pip install Flask
curl -O https://raw.githubusercontent.com/tandav/2ch/master/2ch.py
export FLASK_APP=2ch.py; python3 -m flask run --host=0.0.0.0 &
'''

from flask import Flask
import lib._2ch
import lib._4ch
import string

app = Flask(__name__, static_folder='', static_url_path='')

@app.route('/')
def root():
    return '''\
    <a href='/2ch'>2ch<a>
    <br>
    <a href='/4ch'>4ch<a>
    <br><br>
    <a href='https://github.com/tandav/2ch'>github<a>
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
    ).substitute(threads=x)


@app.route('/2ch')
def get2ch(): return make_html(lib._2ch.html_table())


@app.route('/4ch')
def get4ch(): return make_html(lib._4ch.html_table())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
