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


@app.route('/2ch')
def get2ch(): return lib._2ch.get_html()


@app.route('/4ch')
def get4ch(): return lib._4ch.get_html()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
