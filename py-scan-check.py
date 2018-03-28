from qrcode_scanner import get_info_zxing_qrscanner
from getinfo_check import getinfo_fns

# распознавание qr кода чека
info = get_info_zxing_qrscanner("qrcode.jpg")

#print(info)
#print()

# выделение ФН, ФД, ФПД из даных после распознования qr кода 
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

print("Номер фискального накопителя (ФН) = ", fn)
print("Фискальные данные(ФД) = ", fd)
print("фискальный признак документа(ФПД) = ", fpd)

# получение данных чека в виде json
print(getinfo_fns(fn, fd, fpd).json())