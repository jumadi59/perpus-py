import os
import re
import datetime

def cetakBukti(name, data):
    template = openTamplate("data/template.html")
    
    data["nama_perpus"] = "Perpustakan Ada Ada aja Yeeeeee"

    template = typeObject(template, data)
    filename = f"bukti/{name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    #print(template)
    saveFile(filename, template)
    return filename

def typeObject(template, data):
    template = typeIfElse(template, data)

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

def typeIfElse(template, data): 
    pattern = r'\{if:start ([a-zA-Z0-9!_><= \']+)\}(.+?)\{if:end\}'
    matches = re.findall(pattern, template, re.DOTALL)

    tmp2 = template
    for match in matches:
        key = match[0]
        value = match[1]
        m = re.search(r'!=|==|>=|<=|>|<', key)
        s = key.split(m.group())
        if data[s[0].replace(" ", "")] != None:
            dV = s[0].replace(" ", "")
        print(key)
    
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
    "total_denda": "Rp 10.000",
    "total_bayar": "Rp 10.000",
    "total_kembalian": "Rp 0",
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

#cetakBukti("test", data)
# dtpeng - dtpengemali + 7