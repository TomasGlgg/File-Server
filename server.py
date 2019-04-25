import socket, subprocess, os, logging
from termcolor import colored
from datetime import datetime

def addlog(mode, mes):
    mode = int(mode)
    mes = str(mes)
    a = datetime.today()
    time = ('[' + str(a) + '] ')
    if mode == 1:
        logging.info(time + str(mes))
    elif mode == 2:
        logging.error(time + str(mes))

def send(name):
    addlog(1, 'Starting send file: ' + name)
    try:
        file = open(name, 'rb')
        conn.send(str(1).encode())
    except FileNotFoundError:
        addlog(2, 'File not found: ' + name)
        conn.send(str(2).encode())
        return 2
        exit
    conn.recv(1)
    i = 0
    while True:
        data = file.read(1024)
        if not(data):
            break
        i += 1
        conn.send(data)
        conn.recv(1)

    conn.send('123\|/Done!'.encode())
    ask = conn.recv(2).decode()
    if ask == 'ok':
        addlog(1, 'Finished send packets: ' + str(i))
        return 1
    else:
        addlog(2, 'Error synchronization on ' + str(i) + ' packet')
        return 3

def rec(name):
    addlog(1, 'Starting recv the file: ' + name.decode())
    addlog(1, 'Create file ' + name.decode())
    try:
        file = open(name, 'wb')
        conn.send(str(1).encode())
    except:
        addlog(2, 'Error from create file: ' + name.decode())
        conn.send(str(2).encode())
        return 2
    addlog(1, 'Done')
    print(colored('[+] Done', 'green'))
    print(colored('[*] Recv file', 'yellow'))
    addlog(1, 'Starting recv packets')
    i = 0
    while True:
        data = conn.recv(1024)
        try:
            if '123\|/Done!' in data.decode():
                conn.send('2'.encode())
                addlog(1, 'Finish recv packets: ' + str(i))
                return 1
        except:
            1
        i += 1
        conn.send(str(1).encode())
        file.write(data)

def up(name):
    rtrn = send(name)
    if rtrn == 1:
        print(colored('[+] All done', 'green'))
    elif rtrn == 2:
        print(colored(('[-] Fail to open file: ' + str(name)), 'red'))
        addlog(2, 'Fail to open file: ' + str(name))
    elif rtrn == 3:
        addlog(2, 'Error synchronization')
        print(colored('[-] Error synchronization', 'red'))

def down():
    name = conn.recv(20)
    rtrn = rec(name)
    if rtrn == 1:
        print(colored('[+] All done', 'green'))
    elif rtrn == 2:
        print(colored(('[-] Fail to create file: ' + str(name)), 'red'))

def main():
    mainpsswd = '1234'
    addlog(1, 'New connection: ' + str(conn))
    psswd = conn.recv(20).decode()
    if psswd == mainpsswd:
        addlog(1, 'The password is correct: ' + str(psswd))
        conn.send('1'.encode())
    else:
        addlog(1, 'Wrong password: ' + str(psswd))
        print(colored(('Wrong password: ' + str(psswd)), 'red'))
        conn.send('2'.encode())
        addlog(1, 'Closing connection')
        conn.close()
        return
    conn.recv(1)
    while True:
        proc = subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE)
        data = proc.stdout.read()
        conn.send(data.rstrip())
        cmd = conn.recv(10).decode()
        conn.send(str(1).encode())
        if '1' in cmd:
            print(colored('[*] Uploading file', 'yellow'))
            name = conn.recv(20).decode()
            up(name)
        elif '2' in cmd:
            print(colored('[*] Downloading file', 'yellow'))
            down()
        elif '3' in cmd:
            name = conn.recv(20).decode()
            addlog(1, 'Deleting file: ' + name)
            print(colored(('[*] Deleting file: ' + name), 'red'))
            os.system('del ' + str(name))
            addlog(1, 'Done')
            conn.send(str(1).encode())

logging.basicConfig(filename="log.txt", level=logging.INFO)
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 4444))
        s.listen(1)
        print(colored('[*] Listening for incoming TCP connection', 'yellow'))
        addlog(1, 'Starting listener')
        conn, addr = s.accept()
        conn.settimeout(60)
        print(colored('[*] Connection accept from: ' + str(conn), 'yellow'))
        main()
    except ConnectionAbortedError:
        addlog(1, 'Client close the connection')
    except socket.timeout:
        addlog(1, 'Time out')
        print(colored('Time out', 'yellow'))
    else:
        addlog(2, 'Unknow error')
