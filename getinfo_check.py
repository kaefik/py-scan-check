"""
curl -H 'Authorization: Basic Kzc5MjcyNDA5MDIyOjMwMjA5Ng==' 
-H 'Device-Id: ТУТ_ANDROID_ID' 
-H 'Device-OS: Adnroid 6.0.1' 
-H 'Version: 2' 
-H 'ClientVersion: 1.4.2' 
-H 'Host: proverkacheka.nalog.ru:8888' 
-H 'User-Agent: okhttp/3.0.1' 
--compressed 'http://proverkacheka.nalog.ru:8888/v1/inns/*/kkts/*/fss/XXXXXXXXXXXXXXXX/tickets/YYYYY?fiscalSign=ZZZZZZZZZZ&sendToEmail=no'

XXXXXXXXXXXXXXXX - номер фискального накопителя (ФН)
YYYYY - фискальные данные(ФД)
ZZZZZZZZZZ - фискальный признак документа(ФПД)
"""

import requests
import base64

import click
from  config import Config

"""
пример использования:
    python3 getinfo_check.py 8710000100730663 2860 4249261172
"""

def getinfo_fns(fn, fd, fpd):
    """
        получение данных из ФНС информации используя данные с чека ФН, ФПД, ФД
    """
    cfg = Config()
    strs = "{0}:{1}".format(cfg.username, cfg.code)
    print(strs)
    encoded_authorization = base64.b64encode(strs.encode())
    str_encoded_authorization = "Basic {0}".format(encoded_authorization.decode("utf-8"))

    """
    fn = '8710000100730663' # номер фискального накопителя (ФН)
    fd = '2860'             # фискальные данные(ФД)
    fpd = '4249261172'      # фискальный признак документа(ФПД)

    fn = '8710000100677412' # номер фискального накопителя (ФН)
    fd = '93529'             # фискальные данные(ФД)
    fpd = '2689912220'      # фискальный признак документа(ФПД)
    """

    url = "http://proverkacheka.nalog.ru:8888/v1/inns/*/kkts/*/fss/{0}/tickets/{1}?fiscalSign={2}&sendToEmail=no".format(fn, fd, fpd)

    header_session = {'Authorization': str_encoded_authorization, 'User-Agent': 'okhttp/3.0.1', 'Device-Id': 'android_id', 'Device-OS': 'Adnroid 6.0.1', 'Version': '2', 'ClientVersion': '1.4.2', 'Host': 'proverkacheka.nalog.ru:8888' }

    r = requests.get(url, headers=header_session) 

    if r is None:
        return None  

    return r

@click.command()
@click.argument('fn')
@click.argument('fd')
@click.argument('fpd')
def main(fn, fd, fpd):
    r = getinfo_fns(fn, fd, fpd)
    if r.status_code == 200:
        print("Информация получена: {}".format(r.json()))
    else:
        print("Код ответа от сервера ФНС: {}".format(r.status_code))

if __name__=="__main__":
    main()
    