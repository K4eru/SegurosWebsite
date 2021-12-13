import requests, re

def get_companies():
    url = 'http://127.0.0.1:8001/api/company/'
    r = requests.get(url).json()

    return r

def get_orders():
    url = 'http://127.0.0.1:8001/api/order/'
    r = requests.get(url).json()

    return r

def get_order(id):
    url = 'http://127.0.0.1:8001/api/order/{0}/'.format(id)
    r = requests.get(url).json()

    return r


def get_trainings():
    url = 'http://127.0.0.1:8001/api/training/'
    r = requests.get(url).json()

    return r


def get_checklists():
    url = 'http://127.0.0.1:8001/api/checklist/'
    r = requests.get(url).json()

    return r

def get_checklist(id):
    url = 'http://127.0.0.1:8001/api/checklist/{0}/'.format(id)
    r = requests.get(url).json()

    return r
