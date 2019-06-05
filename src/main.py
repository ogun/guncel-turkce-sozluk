""" Güncel Türkçe Sözlük verilerini kaydeder """
import json

import consts

from pymongo import MongoClient, ReplaceOne
import requests

CLIENT = MongoClient("localhost", 27017)
MONGO_TOPICS = CLIENT.gts.madde
GEVENT_JOBS = []


def get_api_result(word):
    """ GTS uzerinden kelimeyi getirir """

    headers = {
        "User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"
    }

    api_url = f"http://www.sozluk.gov.tr/gts?ara={word}"
    result = requests.get(api_url, headers=headers)

    if result.status_code != 200:
        print("API error. Status Code: {result.status_code}. Word: {word}")
        return None

    return result.text


def get_results():
    """ Elimizdeki kelime listesi uzerinden kelimeleri getirir """
    for word in consts.WORDS:
        response = get_api_result(word)
        if not response:
            continue

        maddeler = json.loads(response)

        for madde in maddeler:
            if not isinstance(madde, dict):
                print(f"Wrong type for: {word}. Detail: {madde}")
                continue

            madde_id = madde["madde_id"]

            mongo_obj = madde.copy()
            mongo_obj["_id"] = madde_id

            MONGO_TOPICS.replace_one({"_id": madde_id}, mongo_obj, upsert=True)


if __name__ == "__main__":
    get_results()
