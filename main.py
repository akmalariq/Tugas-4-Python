def createDatabase():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Input sql root pass: ")
    )

    mycursor = mydb.cursor()

    mycursor.execute(  """  CREATE DATABASE IF NOT EXISTS buku;
                            USE buku;

                            CREATE TABLE users (
                                id_user INT AUTO_INCREMENT,
                                nama_user VARCHAR(50),
                                tgl_lahir DATE,
                                pekerjaan VARCHAR(100),
                                alamat VARCHAR(300),
                                PRIMARY KEY (id_user)
                            );

                            INSERT INTO users VALUES
                            (1, "adi", '2000-01-02', "Mahasiswa", "Jl. Pegangsaan Timur No.56"),
                            (2, "budi", '2000-02-03', "PNS", "Jl. Soekarno Hatta No.37"),
                            (3, "chaniago", '2000-03-04', "Swasta", "Jl. Alwi Abdul Djalil Habibie");

                            CREATE TABLE books (
                                id_buku INT AUTO_INCREMENT,
                                nama_buku VARCHAR(50),
                                kategori VARCHAR(50),
                                stock INT,
                                PRIMARY KEY (id_buku)
                            );

                            INSERT INTO books VALUES
                            (1, "Kitab Pink Jason Ranti", "Biografi", 10),
                            (2, "Cantik Itu Luka", "Novel", 10),
                            (3, "Hello, Cello", "Fiksi", 10);


                            CREATE TABLE peminjaman (
                                id_user INT,
                                id_buku INT,
                                nama_user VARCHAR(50),
                                nama_buku VARCHAR(50),
                                tgl_pinjam DATE,
                                tgl_pengembalian DATE
                            );
                            
                            INSERT INTO peminjaman VALUES
                            (1, 1, "adi", "Kitab Pink Jason Ranti", '2022-07-20', '2022-07-23'),
                            (2, 2, "budi", "Cantik Itu Lukai", '2022-07-21', '2022-07-24'),
                            (3, 3, "chaniago", "Hello, Cello", '2022-07-22', '2022-07-25');""")


def myDB():
    return mysql.connector.connect( host="localhost",
                                    user="root",
                                    password=input("Input sql root pass: "),
                                    database="buku")

def daftarUserBaru():
    nama_user   = str(input("Masukan nama user: "))
    while True:
        try:
            tgl_lahir   = str(input("Masukan tanggal lahir(YYYY-MM-DD): "))
            datetime.datetime.strptime(tgl_lahir, '%Y-%m-%d')
            break
        except:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    pekerjaan   = str(input("Pekerjaan: "))
    alamat      = str(input("Masukan alamat: "))

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO users VALUES (NULL, \"{nama_user}\", '{tgl_lahir}', \"{pekerjaan}\", \"{alamat}\")")
    mydb.commit()
    print(f"Query berhasil ! {mycursor.rowcount} record inserted.")
    

def daftarBukuBaru():
    nama_buku   = str(input("Enter book name: "))
    kategori    = str(input("Masukan kategori: "))
    while True:
            try:
                stock   = int(input("Stok buku: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO books VALUES (NULL, \"{nama_buku}\", \"{kategori}\", {stock})")
    mydb.commit()
    print(f"Query berhasil ! {mycursor.rowcount} record inserted.")

def peminjaman():
    while True:
            try:
                id_user = int(input("Masukan id peminjam: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")
    while True:
            try:
                id_buku = int(input("Masukan id buku: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")
    nama_user = str(input("Masukan nama peminjam: "))
    nama_buku = str(input("Masukan nama buku: "))

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO peminjaman VALUES ({id_user}, {id_buku}, \"{nama_user}\", \"{nama_buku}\", CURDATE(), DATE_ADD(CURDATE(), INTERVAL 3 DAY))")
    mydb.commit()
    print(f"Query berhasil ! {mycursor.rowcount} record inserted.")

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"UPDATE books SET stock=stock-1 WHERE id_buku={id_buku};")
    mydb.commit()


def tampilkanDaftarBuku():
    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM books")
    myresult = mycursor.fetchall()
    print(tabulate([x for x in myresult], headers=['id', 'Judul Buku', 'Kategori', 'Stock']))

def tampilkanDaftarUser():
    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    print(tabulate([x for x in myresult], headers=['id', 'Username','Tanggal Lahir', 'Pekerjaan', 'Alamat']))
    
def tampilkanDaftarPeminjaman():
    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM peminjaman")
    myresult = mycursor.fetchall()
    print(tabulate([x for x in myresult], headers=['User ID', 'Book ID', 'Username','Judul Buku', 'Tanggal Pinjam', "Tanggal Pengembalian"]))

def cariBuku():
    arg = str(input("Masukan nama buku: "))
    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM books WHERE nama_buku LIKE \"%{arg}%\";")
    myresult = mycursor.fetchall()
    print(tabulate([x for x in myresult], headers=['id', 'Judul Buku', 'Kategori', 'Stock']))

def pengembalian():
    while True:
            try:
                id_user = int(input("Masukan id peminjam: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")
    while True:
            try:
                id_buku = int(input("Masukan id buku: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"DELETE FROM peminjaman WHERE id_user={id_user} AND id_buku={id_buku}")
    mydb.commit()
    print(mycursor.rowcount, "record deleted.")

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"UPDATE books SET stock=stock+1 WHERE id_buku={id_buku};")
    mydb.commit()

def actions():
    while True:
        print("""
        ----------LIBRARY MANAGEMENT----------
            \t1. Pendaftaran User Baru
            \t2. Pendaftaran Buku Baru
            \t3. Peminjaman
            \t4. Tampilkan Daftar Buku
            \t5. Tampilkan Daftar User
            \t6. Tampilkan Daftar Peminjaman
            \t7. Cari Buku
            \t8. Pengembalian
            \t9. Exit
        """)
        while True:
            try:
                argument = int(input("Masukan Nomor Tugas: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka dari 1-9!!!\n")
    
        print("")
        if argument == 1:
            daftarUserBaru()
        elif argument == 2:
            daftarBukuBaru()
        elif argument == 3:
            peminjaman()
        elif argument == 4:
            tampilkanDaftarBuku()
        elif argument == 5:
            tampilkanDaftarUser()
        elif argument == 6:
            tampilkanDaftarPeminjaman()
        elif argument == 7:
            cariBuku()
        elif argument == 8:
            pengembalian()
        elif argument == 9:
            exit()
        else:
            print("\n!!!Input salah! Tolong masukan satuan angka dari 1-9!!!\n")

if __name__ == "__main__":
    import os, datetime, mysql.connector
    from tabulate import tabulate

    createDatabase()
    actions()
