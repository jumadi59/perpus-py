import sys
import util
import datetime
import hashlib
import cetak
import pandas as pd
from pwinput import pwinput 

userLogin = ""
dendaPerHari = 5000
maxMeminjam = 5


# Test push git
def getUser(username):
    users = util.openData("data/users.json")
    for user in users:
        if user["username"] == username:
            return user

def home():
    util.clearScreen()
    option = input('''
    ╔════════════════════════════════╗
    ║             welcome            ║
    ╠════════════════════════════════╣
    ║   [1] login                    ║
    ║   [2] registrasi               ║
    ║   [3] keluar                   ║
    ╚════════════════════════════════╝   
    [-] pilih menu selection diatas [1/2/3] 
        input : ''')
    if option == "1" : login()
    elif option == "2" : register()
    elif option == "3" : propExit(home)
    else: wrongInput(home)

def login():
    util.clearScreen()
    print(''' 
    ╔═════════════╗ selamat datang di aplikasi perpus sederhana kami
    ║    login    ║ pastikan kamu sudah benar dalam memasukan input
    ╚═════════════╝ silahkan cek terlebih dahulu sebelum menginputkan ^ ^!''')
    print('''    ╔════════════════════════════════╗''')
    username = input('''     [-] username : ''')
    password = pwinput('''     [-] password : ''') # menyembuninyak password
    print("    ╚════════════════════════════════╝")
    user = {
        "username": username,
        "password": password
    }

    global userLogin
    users = util.openData("data/users.json")
    isLogin = False


    md5Hash = hashlib.md5()
    md5Hash.update(str(password).encode('utf-8'))

    for user in users:
        if user["username"] == username and user["password"] == md5Hash.hexdigest():
            userLogin = user["username"]
            isLogin = True
            break
    
    if isLogin: menu()
    else: 
        print('''    [x] username / password anda salah !''')
        backTo(home)           

def menu():
    util.clearScreen()
    timeLogin = datetime.date.today()
    books = util.openData("data/books.json")
    print('''    [⛑ ] admin           : ''' , getUser(userLogin)["username"] ,
          ''' \n    [🛡 ] masuk pada      : ''', timeLogin,
          ''' \n    [🛠 ] total buku      : ''', len(books))
    option = input(''' 
    ╔════════════════════════════════╗
    ║          PERPUS MENU           ║
    ╠════════════════════════════════╣
    ║   [1] daftar buku              ║
    ║   [2] cari buku                ║
    ║   [3] daftar pinjam buku       ║
    ║   [4] pinjam buku              ║
    ║   [5] kembalikan buku          ║
    ║   [0] keluar                   ║
    ╚════════════════════════════════╝  
    [-] pilih menu selection diatas [1/2/3/4/5/0] 
        input : ''')
    
    if option == "1": daftarBuku()
    elif option == "2": cariBuku()
    elif option == "3": daftarPinjam()
    elif option == "4": 
        if getUser(userLogin)["username"] == "Tamu":
            print('''    [x] silahkan login untuk pinjam buku!''')
            input('''    [note] tekan enter untuk login...''')
            login()
        else:
            pinjamBuku()
    elif option == "5": 
        if getUser(userLogin)["username"] == "Tamu":
            print('''    [x] silahkan login untuk kembalikan buku!''')
            input('''    [note] tekan enter untuk login...''')
            login()
        else:
            kembalikanBuku()
    elif option == "0": propExit(menu)
    else: wrongInput(menu)


def register():
    util.clearScreen()
    print(''' 
    ╔═════════════╗ silahkan membuat username dan password yang baru
    ║  registrasi ║ pastikan kamu sudah benar dalam memasukan input
    ╚═════════════╝ silahkan cek terlebih dahulu sebelum lanjut ^ ^!''')
    print('''    ╔════════════════════════════════╗''')
    username =   input('''     [-] username : ''')
    password = pwinput('''     [-] password : ''')
    nim =        input('''     [-] NIM      : ''')
    print('''    ╚════════════════════════════════╝''')

    md2Hash = hashlib.md5()
    md2Hash.update(str(password).encode('utf-8'))

    if util.getData("data/users.json", "nim", nim) == None:
        util.addData("data/users.json", {
            "username": username,
            "password": md2Hash.hexdigest(),
            "nim": nim
        })
        print('''
        ╔══════════════════════╗ [-] berhasil membuat akun
        ║  registrasi berhasil ║ [-] anda dapat login menggukanan akun yang telah didaftarkan''')
        input('''    ╚══════════════════════╝ [-] tekan enter untuk kembali...''')
        home()
    else:
        print('''    [x] nim yang di input sudah terdaftar !''')
        backTo(home)

def daftarBuku():
    util.clearScreen()
    books = util.openData("data/books.json")
    format = {
        "Code": util.getItemList(books, "code"),
        "Title": util.getItemList(books, "title"),
        "Author": util.getItemList(books, "author"),
        "ISBN": util.getItemList(books, "isbn")
    }
    daftarBukus = pd.DataFrame(format)
    daftarBukus.index = range(1, len(daftarBukus) + 1)


    print('''╔═''', '''═'''*100,'''═╗''', sep= "")
    print(" "*42, "Daftar Buku")
    print('''╚═''', '''═'''*100, '''═╝''', sep="")

    print(daftarBukus)
    backTo(menu)


def cariBuku():
    util.clearScreen()
    search = input("'    [?] cari buku berdasrakan judul : ")
    books = util.openData("data/books.json")
    results = []
    for book in books:
        if book["title"].lower().find(str(search).lower()) != -1:
            results.append(book)
    
    if len(results) > 0:
        for result in results:
            print('''+-----------------------------------------------------------------+''')
            print(f'''\t [-] ID              : {result['id']}''')
            print(f'''\t [-] Kode            : {result['code']}''')
            print(f'''\t [-] Judul           : {result['title']}''')
            print(f'''\t [-] Penerbit        : {result['author']}''')
            print(f'''\t [-] ISBN            : {result['isbn']}''')

        print('''+-----------------------------------------------------------------+''')
        propYesNo("apakah anda ingin mencari buku yang lain", cariBuku, menu)
    else: 
        print(''' 
    ╔═════════════╗ buku yang dicari tidak ditemukan
    ║ input salah ║ coba lagi dengan judul yang tepat ..^ ^! 
    ╚═════════════╝ ''')
        propYesNo("apakah anda ingin mencari buku yang lain", cariBuku, menu)

def pinjamBuku():
    util.clearScreen()
    print('''+------------------------------ pinjam --------------------------+''')
    bookCode = input('''\t [#] kode buku       : ''')

    user = getUser(userLogin)
    books = util.openData("data/books.json")
    result = []
    for book in books:
        if book["code"] == str(bookCode):
            result = book
            break
    if len(result) > 0:
        print('''+-----------------------------------------------------------------+''')
        print(f'''\t [-] Judul           : {result['title']}''')
        print(f'''\t [-] Penerbit        : {result['author']}''')
        print(f'''\t [-] ISBN            : {result['isbn']}''')
        print('''+-----------------------------------------------------------------+''')

        tglPinjam = datetime.date.today().strftime("%d-%m-%Y")
        nimPeminjam     = input('''[-] nim                                     : ''')
        namaPeminjam    = input('''[-] nama peminjam                           : ''')
        tglPinjam       = input('''[-] tanggal pinjam (dd-MM-yyyy)             : ''') 
        tglPengemablian = input('''[-] tanggal harus dikembalikan (dd-MM-yyyy) : ''')

        util.addData("data/peminjam.json", {
            "nim": nimPeminjam,
            "name": namaPeminjam,
            "code_book": result["code"],
            "title_book": result["title"],
            "tgl_pinjam": tglPinjam,
            "tgl_pengembalian": tglPengemablian
        })
        print("[#] data berhasil ditambahkan!")
        propYesNo("apakah anda ingin meminjam buku yang lain", pinjamBuku, menu)

    else:
        print(''' 
    ╔═════════════╗ kode buku yang dicari tidak ditemukan
    ║ input salah ║ coba lagi dengan kode buku yang tepat ..^ ^! 
    ╚═════════════╝ ''')
        propYesNo("apakah anda ingin meminjam buku yang lain", pinjamBuku, menu)

def kembalikanBuku():
    util.clearScreen()

    peminjam = util.openData("data/peminjam.json")

    print('''+-------------- kembalikan buku -------------+''')
    nimPeminjam = input('''[#] NIM peminjam       : ''')
    print('''+--------------------------------------------+''')

    data = []
    for p in peminjam:
        if(p["nim"] == nimPeminjam):
            telatHari = util.hitungTelatBayar(p["tgl_pengembalian"])
            p["telat"] = str(telatHari) + " Hari"
            p["denda"] = util.formatrupiah(telatHari * dendaPerHari)
            data.append(p)

    if len(data) > 0:
        format = {
            "Peminjam": util.getItemList(data, "name"),
            "NIM": util.getItemList(data, "nim"),
            "Kode Buku": util.getItemList(data, "code_book"),
            "Judul buku": util.getItemList(data, "title_book"),
            "Tanggal Pinjam": util.getItemList(data, "tgl_pinjam"),
            "Tanggal Pengembalian": util.getItemList(data, "tgl_pengembalian"),
            "Telat": util.getItemList(data, "telat"),
            "Denda": util.getItemList(data, "denda")
        }
        lisPeminjam = pd.DataFrame(format)
        lisPeminjam.index = range(1, len(lisPeminjam) + 1)


        print('''╔═''', '''═'''*105,'''═╗''', sep= "")
        print(" "*42, "Daftar Pinjam")
        print('''╚═''', '''═'''*105, '''═╝''', sep="")
        if len(data) > 0:
            print(lisPeminjam)
        else:
            print(" "*44, "Empty Data")

        print("")
        kodeBuku = input('''[-] masukan kode buku          : ''')
        result = []
        for book in peminjam:
            if book["code_book"] == str(kodeBuku):
                result = book
                break
        if len(result) > 0:
            telatHari = util.hitungTelatBayar(result["tgl_pengembalian"])
            

            print('''[#] ID peminjam                : ''', result["id"])
            print('''[-] nim                        :''', result["nim"])
            print('''[-] nama peminjam              :''', result["name"])
            print('''[-] tanggal pinjam             :''', result["tgl_pinjam"])
            tglPengemablian = input('''[-] tanggal pengemablian (dd-MM-yyyy) : ''')
            itemCetak = {
                            "kode_buku": result["code_book"],
                            "tgl_pinjam": result["tgl_pinjam"],
                            "tgl_hrs_kembali": str(tglPengemablian),
                            "tgl_pengembalian": result["tgl_pengembalian"],
                            "denda": "-",
                            "jumlah": "-",
                            "keterangan": "",
                    }

            if telatHari > 0:
                print('''[-] Telat                      :''', str(telatHari), "Hari")
                print('''[-] Denda Perhari              :''', util.formatrupiah(dendaPerHari))
                print('''[-] Denda                      :''', util.formatrupiah(telatHari * dendaPerHari))
                uangBayar = input('''[-] Uang Bayar                 : ''')
                uangKembalian = int(uangBayar) - (telatHari * dendaPerHari)
                
                itemCetak["jumlah"] = str(telatHari) + " Hari"
                itemCetak["denda"] = util.formatrupiah(telatHari * dendaPerHari)
            
                if(uangKembalian < 0):
                    print("[?] Nominal bayar terlalu kecil ")
                else:
                    print("[-] Uang Kembali              :", util.formatrupiah(uangKembalian))

            kodePinjam = nimPeminjam.zfill(12)
            util.removeData("data/peminjam.json", result)
            print("")
            print("[#] buku berhasil dikembalikan!")
            file = cetak.cetakBukti(f"bukti_{nimPeminjam}", {
                    "nama_peminjam": "Jumadi Janjaya",
                    "nim": nimPeminjam,
                    "kode_pinjam": kodePinjam,
                    "data_list": [itemCetak]
            })
            util.openBrowser(file)

            backTo(menu)
        else:
            print(''' 
        ╔═════════════╗ 
        ║    Perpus   ║ Kode buku yang dipinjamkan tidak ditemukan, 
        ╚═════════════╝ coba lagi dengan kode buku yang tepat ..^ ^! ''')
            propYesNo("apakah anda ingin mengembaliakn buku yang lain", kembalikanBuku, menu)

    else:
        print(''' 
    ╔═════════════╗ 
    ║    Perpus   ║ Belum ada buku yang anda pinjamkan ..^ ^! 
    ╚═════════════╝ ''')
        propYesNo("apakah anda ingin mengembaliakn buku yang lain", kembalikanBuku, menu)
        

def daftarPinjam():
    util.clearScreen()
    peminjam = util.openData("data/peminjam.json")
    data = []
    for p in peminjam:
        telatHari = util.hitungTelatBayar(p["tgl_pengembalian"])
        p["telat"] = str(telatHari) + " Hari"
        p["denda"] = util.formatrupiah(telatHari * dendaPerHari)
        data.append(p)

    format = {
        "peminjam": util.getItemList(data, "name"),
        "NIM": util.getItemList(data, "nim"),
        "Kode Buku": util.getItemList(data, "code_book"),
        "Judul buku": util.getItemList(data, "title_book"),
        "Tanggal Pinjam": util.getItemList(data, "tgl_pinjam"),
        "Tanggal Pengembalian": util.getItemList(data, "tgl_pengembalian"),
        "Telat": util.getItemList(data, "telat"),
        "Denda": util.getItemList(data, "denda")
    }
    lisPeminjam = pd.DataFrame(format)
    lisPeminjam.index = range(1, len(lisPeminjam) + 1)

    

    print('''╔═''', '''═'''*105,'''═╗''', sep= "")
    print(" "*42, "Daftar Peminjam")
    print('''╚═''', '''═'''*105, '''═╝''', sep="")
    if len(data) > 0:
        print(lisPeminjam)
    else:
        print(" "*44, "Empty Data")
    backTo(menu)

def propExit(callback):
    print('''    ╔════════════════════════════════════════════╗''')
    yesNo = input('''       [!] anda yakin ingin keluar ? [y/t]
    ╚════════════════════════════════════════════╝
    [-] input : ''')
    if yesNo == "y":
        print('''
    [x] -- exit / anda keluar !''')
        sys.exit()
    elif yesNo == "t":
        callback()
    else: wrongInput(callback)

def propYesNo(message, callbackYes, callbackNo):
    print('''    ╔═''', '''═'''*(20 + len(message)),'''═╗''', sep= "")
    print('''       [!] '''+ message +''' ? [y/t]''')
    print('''    ╚═''', '''═'''*(20 + len(message)), '''═╝''', sep="")
    yesNo = input('''   [-] input : ''')
    if yesNo.lower() == "y":
        callbackYes()
    elif yesNo.lower() == "t":
        print('''   [x] -- exit / anda keluar !''')
        callbackNo()


def wrongInput(callback):
        util.clearScreen()
        print('''
        ╔═════════════╗ input kamu tidak diketahui
        ║ input salah ║ coba lagi, jalankan ulang
        ╚═════════════╝ program dan cek kembali ^ ^!
        ''')
        backTo(callback)

def backTo(callback):
    print("\n")
    input('''    [note] tekan enter untuk kembali...''')
    callback()

home()
