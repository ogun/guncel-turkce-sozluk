""" Güncel Türkçe Sözlük verilerini kaydeder """

import logging
from time import sleep

from pymongo import MongoClient
import requests


logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

CLIENT = MongoClient("localhost", 27017)
GTS_DATABASE = CLIENT["gts"]
GTS_MADDELER = GTS_DATABASE["maddeler"]
GTS_MADDE = GTS_DATABASE["madde"]


def add_debug_log(func):
    def wrapper(*args, **kwargs):
        logging.debug(f"{func.__name__} start")
        result = func(*args, **kwargs)
        logging.debug(f"{func.__name__} end")
        return result

    return wrapper


@add_debug_log
def get_maddeler():
    """Sozluk uzerindeki tahmini tum kelimelerin listesini getirir"""

    headers = {
        "User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"
    }

    result = requests.get(
        "https://sozluk.tdk.gov.tr/autocomplete.json", headers=headers
    )
    if result.status_code != 200:
        logging.debug("API error. Status Code: {result.status_code}. Word: {word}")
        return None

    return result.json()


@add_debug_log
def get_api_result(word):
    """GTS uzerinden kelimeyi ceker"""
    headers = {
        "User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"
    }

    api_url = "https://www.sozluk.gov.tr/gts"
    params = {"ara": word}

    try:
        result = requests.get(api_url, params=params, headers=headers, timeout=5)
    except:
        logging.debug("API request error")
        return None

    if result.status_code != 200:
        logging.debug("API error. Status Code: {result.status_code}. Word: {word}")
        return None

    return result.json()


@add_debug_log
def get_results():
    """Elimizdeki kelime listesi uzerinden kelimeleri getirir"""
    word = GTS_MADDELER.find_one({"error": 0})
    if not word:
        logging.debug("Tum kelimeler tamamlandi")
        return False

    kelime = word["madde"]
    logging.debug(f"Looking for: {kelime}")
    maddeler = get_api_result(kelime)
    if not maddeler:
        logging.debug("Istek atarken hata almis, tekrar deneriz hata saymayalim")
        return True

    if "error" in maddeler:
        logging.debug(maddeler)
        GTS_MADDELER.update_one(
            {"_id": word["_id"]},
            {"$set": {"error": word["error"] + 1, "message": "Madde hata verdi"}},
        )
        logging.debug("Madde hata verdi, simdilik koseye alalim seni")
        return True

    for madde in maddeler:
        if not isinstance(madde, dict):
            logging.debug(
                f"{word=} icin beklenmedik durum. dict umduk, su geldi: {madde}"
            )
            continue

        madde_id = int(madde["madde_id"])

        mongo_obj = madde.copy()
        mongo_obj["_id"] = madde_id
        GTS_MADDE.replace_one({"_id": madde_id}, mongo_obj, upsert=True)
        GTS_MADDELER.update_one({"_id": word["_id"]}, {"$set": {"error": -1}})

    return True


@add_debug_log
def create_maddeler():
    """MongoDB koleksiyonlarini, indexlerini falan yoksa yaratalim"""
    db_collections = list(GTS_DATABASE.list_collections())
    if [x for x in db_collections if x.get("name") == "maddeler"]:
        logging.debug("maddeler db is already created")
        return

    GTS_MADDELER.create_index({"madde": 1})
    GTS_MADDELER.create_index({"error": 1})

    maddeler = get_maddeler()
    if not maddeler:
        logging.debug("autocomplete.json dosyasina zeval gelmis")
        return

    GTS_MADDELER.insert_many([{"madde": x["madde"], "error": 0} for x in maddeler])


@add_debug_log
def execute():
    create_maddeler()

    result = True
    while result:
        result = get_results()
        sleep(1)


if __name__ == "__main__":
    execute()
