import requests
import json
import os


def handle(name):
    data = {
        "season": name
    }
    res = requests.post(os.environ["API_URL"] + '/season/fields', data=json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    res = json.loads(res.text)

    return res
