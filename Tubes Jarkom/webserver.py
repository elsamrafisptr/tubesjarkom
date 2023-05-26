from socket import *
import sys
import os

# Membuat TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080  # Nomor port
serverSocket.bind(('', serverPort))  # Mengikat port ke soket
serverSocket.listen(1)  # Menunggu request
print("Ready to serve . . .")

#membuat tipe http agar bisa dipanggil
content_types = {
    "html": "text/html",
    "css" : "text/css"
}

while True:
    connectionSocket, addr = serverSocket.accept()  # Membuat soket koneksi dan menerima request

    try:
        # Menerima message dan mencari file yang diminta
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:], 'rb')  # Open file in binary mode for images
        outputdata = f.read()

        print("File found.")
        # Membuat header bahwa file telah ditemukan dan mengirim file ke klient
        extension = os.path.splitext(filename)[1][1:].lower()
        content_type = content_types.get(extension, "application/octet-stream")
        header = "HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n".format(content_type)
        response = header.encode()+outputdata
        connectionSocket.send(response)

        # Memutuskan koneksi
        print("File sent.")
        connectionSocket.close()

    except IOError:
        # Membuat header error
        error = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        response1 = error.encode()
        connectionSocket.send(response1)

        # Mencari file error dan mengirim file error
        ferr = open("404.html", 'rb')
        outputerr = ferr.read()
        ferr.close()

        # Memutuskan koneksi
        print("Error message sent.")
        connectionSocket.close()

# Tutup aplikasi
serverSocket.close()
sys.exit()
