""" Güncel Türkçe Sözlük verilerini kaydeder """
import logging

from pymongo import MongoClient
import requests


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

CLIENT = MongoClient()
MONGO_TOPICS = CLIENT.gts.madde


def logged(func):
    def log_it(*args, **kwargs):
        logging.info(f"{func.__name__}: start")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__}: end")
        return result

    return log_it


def get_api_result(id):
    """GTS uzerinden kelimeyi getirir"""

    headers = {
        "User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"
    }

    api_url = "https://www.sozluk.gov.tr/gts_id"
    params = {"id": id}
    result = requests.get(api_url, params=params, headers=headers)

    if result.status_code != 200:
        logging.error(f"get_api_result: {result.status_code=} {id=}")
        return None

    return result.json()


@logged
def get_missing_ids():
    available_ids = list(range(1, 92415))

    db_ids = [i["_id"] for i in list(MONGO_TOPICS.find({}, {"_id": 1}))]

    return [i for i in available_ids if str(i) not in db_ids]


@logged
def execute():
    ids = get_missing_ids()

    for id in ids:
        if id % 100 == 0:
            logging.info(f"Getting data for gts_id={id}")

        maddeler = get_api_result(id)
        if "error" in maddeler:
            logging.error(f"Error while getting data for gts_id={id}")
            continue

        for madde in maddeler:
            if not isinstance(madde, dict):
                logging.error(f"Wrong type for: {id}. Detail: {madde}")
                continue

            madde_id = madde["madde_id"]

            mongo_obj = madde.copy()
            mongo_obj["_id"] = madde_id

            MONGO_TOPICS.replace_one({"_id": madde_id}, mongo_obj, upsert=True)


if __name__ == "__main__":
    execute()
