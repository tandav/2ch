'''
https://2ch.hk/api/index.html
https://github.com/4chan/4chan-API
TODO: githooks (git push github, git push prod) / or git hooks on github

sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
python3 -m pip install Flask
sudo apt install git-all 
git clone https://github.com/tandav/2ch.git
cd 2ch
python3 server.py
'''

from flask import Flask, request
from lib import _2ch, _4ch, util


app = Flask(__name__, static_folder='', static_url_path='')


@app.route('/')
def root():
    return '''
    <a href='/2ch'>2ch<a>
    <br>
    <a href='/4ch'>4ch<a>
    <br><br>
    <a href='https://github.com/tandav/2ch'>github<a>
    '''


@app.route('/2ch')
def get2ch(): return util.get_html(_2ch, request.args.get('sortby', default='posts_count'))


@app.route('/4ch')
def get4ch(): return util.get_html(_4ch, request.args.get('sortby', default='posts_count'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
