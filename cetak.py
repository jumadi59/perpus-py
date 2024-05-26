import os
import re
import datetime

def cetakBukti(name, data):
    template = openTamplate("data/template.html")
    template = typeObject(template, data)
    filename = f"bukti/{name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    saveFile(filename, template)
    return filename

def typeObject(template, data):
    for key, value in data.items():
        if type(value) is list:
            template = typeList(template, key, value)
        else:
            template = typeString(template, key, value)
    
    return template

def typeString(template, key, value):
    return template.replace("{" + key +"}", value)

def typeList(template, key, list):
    pattern = r'\{for:start ' + key + r'\}(.+?)\{for:end\}'
    matches = re.findall(pattern, template, re.DOTALL)
    tmpStart = template[0:(template.index("{for:start "+key+"}"))]
    tmp2 = ""
    tmpEnd = template[(template.index("{for:end}")+9):len(template)]
    for match in matches:
        strip = match.strip()
        for item in list:
            tmp2 +=typeObject(strip, item)
        
    return tmpStart + tmp2 + tmpEnd

def typeBoolean(template, key, bool):
    return template

def openTamplate(fileName) :
    path = os.getcwd() + "/" + fileName
    content = ""
    with open(path, 'r') as file:
        content = file.read()
        
    return content

def saveFile(fileName, template):
    path = os.getcwd() + "/" + fileName

    with open(path , "w") as file:
        file.write(template)

data = {
    "nama_peminjam": "Jumadi Janjaya",
    "nim": "17235050",
    "kode_pinjam": "LTEW9GWRFT",
    "data_list": [
        {
            "kode_buku": "LTEW9GWRFT",
            "tgl_pinjam": "18-05-2024",
            "tgl_hrs_kembali": "26-05-2024",
            "tgl_pengembalian": "22-05-2024",
            "denda": "Rp 5000",
            "jumlah": "1 Hari",
            "keterangan": "",
        },
        {
            "kode_buku": "LTEW9GWRFT",
            "tgl_pinjam": "18-05-2024",
            "tgl_hrs_kembali": "26-05-2024",
            "tgl_pengembalian": "22-05-2024",
            "denda": "Rp 5000",
            "jumlah": "1 Hari",
            "keterangan": "",
        },
        {
            "kode_buku": "LTEW9GWRFT",
            "tgl_pinjam": "18-05-2024",
            "tgl_hrs_kembali": "26-05-2024",
            "tgl_pengembalian": "22-05-2024",
            "denda": "Rp 5000",
            "jumlah": "1 Hari",
            "keterangan": "",
        }
    ]
}