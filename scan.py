"""
curl -H 'Authorization: Basic Kzc5MjcyNDA5MDIyOjMwMjA5Ng==' 
-H 'Device-Id: ТУТ_ANDROID_ID' 
-H 'Device-OS: Adnroid 6.0.1' 
-H 'Version: 2' 
-H 'ClientVersion: 1.4.2' 
-H 'Host: proverkacheka.nalog.ru:8888' 
-H 'User-Agent: okhttp/3.0.1' 
--compressed 'http://proverkacheka.nalog.ru:8888/v1/inns/*/kkts/*/fss/8710000100730663/tickets/2860?fiscalSign=4249261172&sendToEmail=no'

XXXXXXXXXXXXXXXX - номер фискального накопителя (ФН)
YYYYY - фискальные данные(ФД)
ZZZZZZZZZZ - фискальный признак документа(ФПД)
"""

import requests
import base64

from  config import Config

cfg = Config()
strs = "{0}:{1}".format(cfg.username, cfg.code)
# print(strs)
encoded_authorization = base64.b64encode(strs.encode())
str_encoded_authorization = "Basic {0}".format(encoded_authorization.decode("utf-8"))

"""
fn = '8710000100730663' # номер фискального накопителя (ФН)
fd = '2860'             # фискальные данные(ФД)
fpd = '4249261172'      # фискальный признак документа(ФПД)
"""

fn = '8710000100677412' # номер фискального накопителя (ФН)
fd = '93529'             # фискальные данные(ФД)
fpd = '2689912220'      # фискальный признак документа(ФПД)


url = "http://proverkacheka.nalog.ru:8888/v1/inns/*/kkts/*/fss/{0}/tickets/{1}?fiscalSign={2}&sendToEmail=no".format(fn, fd, fpd)

header_session = {'Authorization': str_encoded_authorization, 'User-Agent': 'okhttp/3.0.1', 'Device-Id': 'android_id', 'Device-OS': 'Adnroid 6.0.1', 'Version': '2', 'ClientVersion': '1.4.2', 'Host': 'proverkacheka.nalog.ru:8888' }

r = requests.get(url, headers=header_session) 

print(r)
print(r.json())