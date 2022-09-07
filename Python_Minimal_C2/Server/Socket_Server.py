import socket
import threading
from datetime import date, datetime
import os


#threading info https://www.geeksforgeeks.org/multithreading-python-set-1/

#write data to the end of a log file
def write_log(data):
    f = open ('C:\Windows\Tasks\log.txt', 'a+')
    f.seek(0,2)
    f.write(data + "\n")
    f.close()

# get date and time; for logging
def get_current_time():
     now_time = datetime.now()
     current_time = now_time.strftime("%H:%M:%S")
     today = date.today()
     output = f"{today} {current_time}"
     return output

def get_current_time_for_file_name():
     now_time = datetime.now()
     current_time = now_time.strftime("%H%M%S")
     today = date.today()
     output = f"{today}_{current_time}"
     return output

#Create and return socket
def create_socket(port):
     addr = ("0.0.0.0", port)
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     sock.bind(addr)
     sock.listen()

     # print and log socket
     print(f"started socket on port: {port}")
     log = f"{get_current_time()}:  Started socket on port: {port}" 
     write_log(log)
     return sock

#Method for handling beacons
def start_beacon(port):
    sock = create_socket(port)

    while True:
        conn, addr = sock.accept()
        print(f"Connection from {addr}")
        write_log(f"Connection from {addr}")
        while True:
            data = conn.recv(1024).decode('UTF-8')
            if not data:
                break
            write_log(data)
            print(data)
        conn.close() 

# Method for receiving files        
def start_file_receiver(port):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096

    sock = create_socket(port)
    while True:
        # accept connection if there is any
        conn, addr = sock.accept()
        write_log(f"Connection from {addr}")
        print(f"[+] {addr} is connected.")
    
        # receive the file infos
        # receive using client socket, not server socket
        received = conn.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        write_log(f"Receiving file {filename}, size {filesize}")

        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        unique_name = get_current_time_for_file_name()
        unique_log_name = f"C:\Windows\Tasks\{unique_name}.zip"
        # start receiving the file from the socket
        # and writing to the file stream
        ## Need to add check that the file doesn't exist or create unqiue name
        with open(unique_log_name, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = conn.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
            conn.close()

        # close the client socket
        print(sock)
        




thread1 = threading.Thread(target=start_beacon, args=(8443,))
thread2 = threading.Thread(target=start_file_receiver, args=(8444,))

thread1.start()
thread2.start()

