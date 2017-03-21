import datetime
import requests
import request_helper


def get():
    t = datetime.date.today()
    today = t.strftime('%Y-%m-%d')
    endpoint = request_helper.makeEndpoint()
    headers = request_helper.makeHeaders()
    return requests.get(endpoint, date=today, headers=headers)


def post(date):
    endpoint = request_helper.makeEndpoint()
    headers = request_helper.makeHeaders()
    return requests.post(endpoint, date, headers=headers)


def delete(date):
    endpoint = request_helper.makeEndpoint()
    headers = request_helper.makeHeaders()
    return requests.delete(endpoint, date, headers=headers)


