#!/usr/bin/env python3
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from configparser import ConfigParser
import os

def getDuration(location):
    conf = ConfigParser()
    parDir = os.path.dirname(os.path.abspath(__file__))
    conf.read(os.path.join(parDir, 'metroCode.ini'), encoding='utf8')
    sta = conf['station']
    url = ('http://web.metro.taipei/c/2stainfo.asp?s1elect={}&action=query&s2elect={}&submit=%C2%A0%E7%A2%BA%E5%AE%9A%C2%A0'.
        format(sta[location[0]], sta[location[1]]))
    rawData = urlopen(url)
    
    soup = BeautifulSoup(rawData, 'html.parser')
    divided = soup.find_all('div')

    # parse all kind of prices at 4, 5, 6
    prices = []
    for i in divided[4:7]:
        prices.append(i.get_text())

    # parse duration and how to change line at 11, 12
    duration = divided[11].get_text()
    howto = divided[12].get_text()

    display = '{} => {}\n'.format(location[0], location[1])
    display += '票價\n'
    display += '單程票: {}\n'.format(prices[0])
    display += '電子票證: {}\n'.format(prices[1])
    display += '敬老卡、愛心卡、愛心陪伴卡: {}\n'.format(prices[2])
    display += '乘車時間: {}\n'.format(duration)
    display += '乘車方式: {}'.format(howto)

    return display

if __name__ == '__main__':
    location = ['六張犁', '台北車站']
    print(getDuration(location))
