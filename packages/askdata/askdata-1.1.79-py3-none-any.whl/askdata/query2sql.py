from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import requests


def query_to_sql(smartquery, db_driver):

    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = "https://api-dev.askdata.com/query2sql/query_to_sql"

    data = {
        "smartquery": smartquery,
        "db_driver": db_driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        translation = dict_response['translation']
        return translation
    except Exception as e:
        logging.error(str(e))
