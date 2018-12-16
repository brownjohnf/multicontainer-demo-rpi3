#!/user/bin/env python

from bs4 import BeautifulSoup
import urllib.request
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def get():
    raw_html = urllib.request.urlopen('http://199.191.49.179/where/iphone/stop.action?id=1_31736&route=1_100019').read()

    html = BeautifulSoup(raw_html)

    html.find('div', id='topBar' ).extract()
    html.find('div', class_='arrivalsFilterPanel' ).extract()
    html.find('div', id='nearby_stops' ).extract()
    html.find('div', class_='agenciesSection' ).extract()
    for ul in html.find_all('ul', class_='buttons' ):
        ul.extract()

    return str(html)

@app.route('/<path>')
def catchall(path):
    url = 'http://199.191.49.179/' + request.url
    print(url)
    return urllib.request.urlopen(url).read()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
