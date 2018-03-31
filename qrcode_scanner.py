import requests

path_test = "data_check_test/"

def qrcode_scanner(url, filename):
    """
        отправляет запрос в онлайн сканер qr кодов и получает ответ от сервера (Отправка файла через Request Payload)
        url - ссылка на скрипт онлайн сканера
        filename  - путь до файла снимка где находится фотография с qr кодом
    """
    result = {}
    with open(filename, 'rb') as f: 
        r = requests.post(url, files={filename: f})
        result = {"code":r.status_code, "text": r.text}
    return result


def get_info_zxing_qrscanner(filen):
    url = "https://zxing.org/w/decode"
    # filen = "test.png"
    # filen = "qrcode.jpg"
    rr = qrcode_scanner(url, filen)
    #print(rr["code"])
    #print(rr["text"])

    s = rr["text"]
    i = s.find("pre")
    s = s[i+4:]
    i = s.find("pre")
    s = s[:i]
    s =s.strip("/")
    s =s.strip("<")
    s =s.strip(">")
    return s

if __name__ == "__main__":
    print(get_info_zxing_qrscanner(path_test + "qrcode.jpg"))