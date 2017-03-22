import datetime
import requests
import request_helper
import argparse
import logging
import json

logging.basicConfig(filename='holiday.log', level=logging.INFO)
t = datetime.date.today()
today = t.strftime('%Y-%m-%d')


def get(date):
    params = "date=" + date
    url = request_helper.make_endpoint(params)
    headers = request_helper.make_headers("GET", "", params)
    response = requests.get(url, headers=headers)
    if response.ok:
        res = response.json()
        for item in res:
            logging.debug(item + ': ' + str(res[item]))
        if res['Count'] == 1:
            return True
        else:
            return False
    else:
        return False


def get_all():
    params = "all=true"
    url = request_helper.make_endpoint(params)
    headers = request_helper.make_headers("GET", "", params)
    response = requests.get(url, headers=headers)
    if response.ok:
        res = response.json()
        return res['Items']


def post(date):
    json_data = '"' + date + '"'
    logging.debug("json_data: %s ", json_data)
    endpoint = request_helper.make_endpoint("")
    headers = request_helper.make_headers("POST", json_data, "")
    response = requests.post(endpoint, data=json_data, headers=headers)
    if response.ok:
        logging.info("The day %s is a holiday now.", date)
    else:
        logging.info("Set holiday failure." + response.text)


def delete(date):
    json_data = '"' + date + '"'
    endpoint = request_helper.make_endpoint("")
    headers = request_helper.make_headers("DELETE", json_data, "")
    response = requests.delete(endpoint, data=json_data, headers=headers)
    if response.ok:
        logging.info("The day %s is not a holiday anymore.", date)
    else:
        logging.info("Revert holiday failure." + response.text)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", nargs="?", default=today, help="Get the status of the specified date")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--all", nargs="?", const=today, help="List all holidays")
    group.add_argument("-p", "--post", nargs="?", const=today, help="Mark the specified day as a holiday")
    group.add_argument("-d", "--delete", nargs="?", const=today, help="Revert the holiday")
    args = parser.parse_args()

    if args.all is not None:
        logging.info(json.dumps(get_all(), sort_keys=True, indent=4, separators=(',', ': ')))
    elif args.post is not None:
        # TODO check date format
        post(args.post)
    elif args.delete is not None:
        # TODO check date format
        delete(args.delete)
    else:
        info = get(args.date)
        logging.info("The day %s is holiday: %s", args.date, info)

if __name__ == "__main__":
    run()
