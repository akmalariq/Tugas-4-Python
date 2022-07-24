def createDatabase():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TxnqyeY4njLuQ5ZB*"
    )

    mycursor = mydb.cursor()

    mycursor.execute(  """  DROP DATABASE IF EXISTS buku;
                            CREATE DATABASE IF NOT EXISTS buku;
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
                            (1, "Kitab Pink Jason Ranti", "Biografi", 9),
                            (2, "Cantik Itu Luka", "Novel", 9),
                            (3, "Hello, Cello", "Fiksi", 9);


                            CREATE TABLE peminjaman (
                                id_user INT,
                                id_buku INT,
                                nama_user VARCHAR(50),
                                nama_buku VARCHAR(50),
                                tgl_pinjam DATE
                            );

                            INSERT INTO peminjaman VALUES
                            (1, 1, "adi", "Kitab Pink Jason Ranti", '2022-07-20'),
                            (2, 2, "budi", "Cantik Itu Lukai", '2022-07-21'),
                            (3, 3, "chaniago", "Hello, Cello", '2022-07-22');""")


def myDB():
    return mysql.connector.connect( host="localhost",
                                    user="root",
                                    password="TxnqyeY4njLuQ5ZB*",
                                    database="buku")

def daftarUserBaru():
    username    = str(input("Masukan nama user: "))
    birthdate   = str(input("Masukan tanggal lahir(YYYY-MM-DD): "))
    pekerjaan   = str(input("Pekerjaan: "))
    alamat      = str(input("Masukan alamat: "))

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO users VALUES (NULL, \"{username}\", '{birthdate}', \"{pekerjaan}\", \"{alamat}\")")

    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    

def daftarBukuBaru():
    title    = str(input("Enter book name: "))
    kategori   = str(input("Masukan kategori: "))
    while True:
            try:
                stock   = int(input("Stok buku: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")

    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO books VALUES (NULL, \"{title}\", \"{kategori}\", {stock})")

    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def peminjaman():
    print("World")

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
    print(tabulate([x for x in myresult], headers=['id', 'Username','tanggal_lahir', 'Pekerjaan', 'Alamat']))
    
def tampilkanDaftarPeminjaman():
    mydb = myDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM peminjaman")
    myresult = mycursor.fetchall()
    print(tabulate([x for x in myresult], headers=['User ID', 'Book ID', 'Username','Judul Buku', 'Tanggal Pinjam']))

def cariBuku():
    print("World")

def pengembalian():
    print("World")

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
    import os
    import mysql.connector
    from tabulate import tabulate

    createDatabase()
    actions()