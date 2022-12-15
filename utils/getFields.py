import requests
import json
import os


def handle(season_id):
    res = requests.get(os.environ["API_URL"] + f'/seasons/{season_id}/fields', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    res = json.loads(res.text)

    return res
