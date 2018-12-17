#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib.request
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def get():
    stop = request.args.get('stop')
    route = request.args.get('route')

    url = 'http://199.191.49.179/where/iphone/stop.action?id=1_' + \
        stop + \
        '&route=1_' + \
        route

    raw_html = urllib.request.urlopen(url).read()
    html = BeautifulSoup(raw_html)

    html.find('div', id='topBar' ).extract()
    html.find('div', class_='arrivalsFilterPanel' ).extract()
    html.find('div', id='nearby_stops' ).extract()
    html.find('div', class_='agenciesSection' ).extract()
    for ul in html.find_all('ul', class_='buttons' ):
        ul.extract()

    for tr in html.find_all('tr', class_='arrivalsRow'):
        td = tr.find('td', class_='arrivalsStatusEntry')

        try:
            if int(td.string) < 0:
                print('--> Removing negative time: ' + td.string)
                tr.extract()
        except:
            print('--> Ignoring non-int: ' + td.string)
            None

    return str(html)

@app.route('/<path>')
def catchall(path):
    url = 'http://199.191.49.179/' + request.url
    return urllib.request.urlopen(url).read()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
