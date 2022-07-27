def createDatabase(SQLpass):
    conn = mysql.connector.connect(host="localhost", user="root", password=SQLpass)
    cursor = conn.cursor()
    sql = """ 
            DROP DATABASE IF EXISTS buku;
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
        """
    cursor.execute(sql)
    cursor.close()
    conn.close()


def Conn(SQLpass):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=SQLpass,
        database="buku",
    )


def daftarUserBaru(SQLpass):
    nama_user = str(input("Masukan nama user: "))
    while True:
        try:
            tgl_lahir = str(input("Masukan tanggal lahir(YYYY-MM-DD): "))
            datetime.datetime.strptime(tgl_lahir, "%Y-%m-%d")
            break
        except:
            print("Incorrect data format, should be YYYY-MM-DD")
    pekerjaan = str(input("Pekerjaan: "))
    alamat = str(input("Masukan alamat: "))

    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO users VALUES (NULL, "{nama_user}", \'{tgl_lahir}\', "{pekerjaan}", "{alamat}")'
    )
    conn.commit()
    print(f"Query berhasil ! {cursor.rowcount} record inserted.")
    cursor.close()
    conn.close()


def daftarBukuBaru(SQLpass):
    nama_buku = str(input("Enter book name: "))
    kategori = str(input("Masukan kategori: "))
    while True:
        try:
            stock = int(input("Stok buku: "))
            break
        except:
            print("\n!!!Input salah! Tolong masukan satuan angka!!!\n")

    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO books VALUES (NULL, "{nama_buku}", "{kategori}", {stock})'
    )
    conn.commit()
    print(f"Query berhasil ! {cursor.rowcount} record inserted.")
    cursor.close()
    conn.close()


def peminjaman(SQLpass):
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

    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO peminjaman VALUES ({id_user}, {id_buku}, "{nama_user}", "{nama_buku}", CURDATE(), DATE_ADD(CURDATE(), INTERVAL 3 DAY))'
    )
    conn.commit()
    print(f"Query berhasil ! {cursor.rowcount} record inserted.")

    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE books SET stock=stock-1 WHERE id_buku={id_buku};")
    conn.commit()
    cursor.close()
    conn.close()


def tampilkanDaftarBuku(SQLpass):
    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    myresult = cursor.fetchall()
    cursor.close()
    conn.close()
    print(
        tabulate(
            [x for x in myresult], headers=["id", "Judul Buku", "Kategori", "Stock"]
        )
    )


def tampilkanDaftarUser(SQLpass):
    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    cursor.close()
    conn.close()
    print(
        tabulate(
            [x for x in myresult],
            headers=["id", "Username", "Tanggal Lahir", "Pekerjaan", "Alamat"],
        )
    )


def tampilkanDaftarPeminjaman(SQLpass):
    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peminjaman")
    myresult = cursor.fetchall()
    cursor.close()
    conn.close()
    print(
        tabulate(
            [x for x in myresult],
            headers=[
                "User ID",
                "Book ID",
                "Username",
                "Judul Buku",
                "Tanggal Pinjam",
                "Tanggal Pengembalian",
            ],
        )
    )


def cariBuku(SQLpass):
    arg = str(input("Masukan nama buku: "))
    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM books WHERE nama_buku LIKE "%{arg}%";')
    myresult = cursor.fetchall()
    cursor.close()
    conn.close()
    print(
        tabulate(
            [x for x in myresult], headers=["id", "Judul Buku", "Kategori", "Stock"]
        )
    )


def pengembalian(SQLpass):
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

    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(
        f"DELETE FROM peminjaman WHERE id_user={id_user} AND id_buku={id_buku}"
    )
    conn.commit()
    print(cursor.rowcount, "record deleted.")

    conn = Conn(SQLpass)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE books SET stock=stock+1 WHERE id_buku={id_buku};")
    conn.commit()
    cursor.close()
    conn.close()


def actions(SQLpass):
    while True:
        print(
            """
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
        """
        )
        while True:
            try:
                argument = int(input("Masukan Nomor Tugas: "))
                break
            except:
                print("\n!!!Input salah! Tolong masukan satuan angka dari 1-9!!!\n")

        print("")
        if argument == 1:
            daftarUserBaru(SQLpass)
        elif argument == 2:
            daftarBukuBaru(SQLpass)
        elif argument == 3:
            peminjaman(SQLpass)
        elif argument == 4:
            tampilkanDaftarBuku(SQLpass)
        elif argument == 5:
            tampilkanDaftarUser(SQLpass)
        elif argument == 6:
            tampilkanDaftarPeminjaman(SQLpass)
        elif argument == 7:
            cariBuku(SQLpass)
        elif argument == 8:
            pengembalian(SQLpass)
        elif argument == 9:
            exit()
        else:
            print("\n!!!Input salah! Tolong masukan satuan angka dari 1-9!!!\n")


if __name__ == "__main__":
    import os, datetime, mysql.connector
    from tabulate import tabulate

    SQLpass = input("Please input your sql password: ")
    createDatabase(SQLpass)
    actions(SQLpass)
