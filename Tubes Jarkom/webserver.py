from socket import *    # Mengimport modul socket
import sys              # Mengimport sys yang berguna untuk menghentikan program
import os               # Mengimport os yang berguna untuk manipulasi file, direktori, dan variabel lingkungan, serta mengakses informasi sistem

# Membuat TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)     # Membuat socet TCP dengan memanggil fungsi socket dan disimpan di variabel serverSocket
serverPort = 8080                               # Nomor port
serverSocket.bind(('', serverPort))             # Mengikat port ke soket
serverSocket.listen(1)                          # Menunggu request
print("Ready to serve . . .")                   # Mencetak pesan "Ready to serve . . ."

# membuat tipe, agar bisa dipanggil saat dicari.
content_types = {
    "html": "text/html",
    "css" : "text/css",
    "png" : "image/png"
}

while True:
    connectionSocket, addr = serverSocket.accept()     # Membuat soket koneksi dan menerima request

    try:                                               # Mencoba menjalankan code yang berguna untuk mencari dan mengambil file dari file system
        # Menerima message dan mencari file yang diminta
        message = connectionSocket.recv(1024).decode() # Memasukkan paket ke yang sudah tiba kedalam variabel message dan mengkonversikan paketnya dari byte ke tipe data yang normal
        filename = message.split()[1]                  # Memasukkan value dengan indeks ke 1 dari message yang sudah displit kedalam variabel filename
        f = open(filename[1:], 'rb')                   # Membuka file dengan nama yang diambil dari variabel filename
        outputdata = f.read()                          # Membaca konten dari file f ke variabel outputdata

        print("File found.")                           # Mencetak pesan "File found."
        # Membuat header bahwa file telah ditemukan dan mengirim file
        extension = os.path.splitext(filename)[1][1:]                       # Mengambil ekstensi file dari filename yang diberikan
        content_type = content_types.get(extension, "application/octet-stream")         # Menginisialisasi variabel content_type dengan tipe konten berdasarkan ekstensi file
        header = "HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n".format(content_type)     # Membuat string header yang akan menjadi bagian awal dari respons HTTP
        response = header.encode()+outputdata                                           # Menggabungkan string header dengan outputdata yang akan dikirim sebagai respons HTTP
        connectionSocket.send(response)                                                 # Mengirimkan response ke connectionSocket yang merupakan socket koneksi dengan klien

        # Memutuskan koneksi
        print("File sent.")             # Mencetak pesan "File sent."
        connectionSocket.close()        # Menutup koneksi soket connectionSocket

    except IOError:                                                             # Menjalankan code jika codingan pada blok try error (jika file tidak ditemukan)
        # Membuat header error
        error = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"     # Membuat string error yang akan menjadi header respons HTTP dalam kasus file tidak ditemukan
        response1 = error.encode()                                              # Mengubah string error menjadi bentuk byte menggunakan metode encode()
        connectionSocket.send(response1)                                        # Mengirimkan respons HTTP yang berisi header error ke connectionSocket yang merupakan socket koneksi dengan klien

        # Mencari file error dan mengirim file error
        ferr = open("404.html", 'rb')                                            # Membuka file "404.html" dalam mode baca ('r')
        outputerr = ferr.read()                                                 # Membaca seluruh isi file yang dibuka (ferr) dan menyimpannya dalam variabel outputerr
        ferr.close()                                                            # Menutup file yang telah dibuka (ferr)

        # Memutuskan koneksi
        print("Error message sent.")                                            # Mencetak pesan "Error message sent."
        connectionSocket.close()                                                # Menutup koneksi soket ConnectionSocket

# Tutup aplikasi
serverSocket.close()    # Menutup koneksi soket serverSocket
sys.exit()              # Mengakhiri program dengan metode exit()
