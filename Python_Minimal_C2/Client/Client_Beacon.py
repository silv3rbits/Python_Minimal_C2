import socket

# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
port = 8443

##
## Send beacon to Target
##
def send_beacon():
    # create the client socket
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))


    # send the filename and filesize
    message = "Still here!"
    s.sendall(message.encode())

    # close the socket
    s.close()

send_beacon()


