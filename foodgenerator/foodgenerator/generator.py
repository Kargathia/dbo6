"""
Generates raw random data
"""

import os
import random
import requests
from subprocess import call
from subprocess import Popen, PIPE


class Product():
    name = None
    category = None
    priceInCents = None

    def __init__(self, name, category, priceInCents):
        self.name = name
        self.category = category
        self.priceInCents = priceInCents

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.category, self.priceInCents)


def install_lib():
    call(['npm', 'install', 'foody'], shell=True, cwd=os.getcwd())


def generate_products(num,
                      categories=None,
                      min_price_ct=50,
                      max_price_ct=1000):
    if not categories:
        categories = ['FOOD', 'DRINK', 'OTHER']

    dir_name = os.path.abspath(os.getcwd() + '/node_modules/.bin/')

    with Popen(['foody', '-n', str(num)],
               shell=True,
               cwd=dir_name,
               stdout=PIPE,
               bufsize=1,
               universal_newlines=True) as p:
        for line in p.stdout:
            yield Product(line.strip(),
                          random.choice(categories),
                          random.randint(min_price_ct, max_price_ct))


def call_api(url, product):
    response = requests.post(url + '/stock/products', json=product.__dict__)
    assert response.status_code == 100
