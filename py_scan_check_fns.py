from qrcode_scanner import get_info_zxing_qrscanner
from getinfo_check import getinfo_fns



def parse_result_scan_qrcode(info):
    """
    выделение ФН, ФД, ФПД из даных после распознования qr кода 
    """
    info = info.split(";")
    info_dict = {}
    for el in info:
        s = el.split("=")
        info_dict[s[0]] = s[1]
    #print('info = ',info)
    #print('info_dict = ', info_dict)
    fn = info_dict['fn'].split("&")[0]
    fd = info_dict['i'].split("&")[0]
    fpd = info_dict['fp'].split("&")[0]
    return {'fn': fn, 'fd': fd, 'fpd': fpd}

def py_scan_check(filename):
    """
     1. распознование qr кода
     2. выделение нужных частей ФН, ФПД, ФД
     3. получение данных из ФНС используя ФН, ФПД, ФД
    """
    result = None
    # распознавание qr кода чека
    info = get_info_zxing_qrscanner(filename)
    print("Данные после распознования: ", info)

    try:
        result_parse = parse_result_scan_qrcode(info)
    except IndexError:
        return None
    
    # print("Номер фискального накопителя (ФН) = ", result_parse['fn'])
    # print("Фискальные данные(ФД) = ", result_parse['fd'])
    # print("фискальный признак документа(ФПД) = ", result_parse['fpd'])

    # получение данных чека в виде json
    result = getinfo_fns(result_parse['fn'], result_parse['fd'], result_parse['fpd'])
    return result

if __name__ == "__main__":
    path_test = "data_check_test/"
    filen = path_test+"qrcode.jpg"
    filen1 = "data_check/1.jpg"

    r = py_scan_check(filen1)
    print(r.status_code)
    print(r.json())
    