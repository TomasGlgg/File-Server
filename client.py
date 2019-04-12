import socket, subprocess, time
from termcolor import colored
passw = '1234'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)
s.connect((input('IP>'), 4444))
s.send(passw.encode())

def down():
    name = input(colored('Choose file name>', 'yellow'))
    s.send(name.encode())
    data = s.recv(1).decode()

    if  data == str(2):
        print(colored('[-] Error open', 'red'))
        exit()

    s.send(str(1).encode())
    print(colored('[*] Create file', 'yellow'))
    file = open(name, 'wb')
    print(colored('[+] Done', 'green'))
    print(colored('[*] Recv file', 'yellow'))

    while True:
        data = s.recv(1024)
        try:
            if '123\|/Done!' in data.decode():
                break
        except:
            1
        file.write(data)
        s.send(str(1).encode())
    s.send(str('ok').encode())
    print(colored('[+] Done', 'green'))

if str(1) in s.recv(1).decode():
    print(colored('[+] PWD!', 'green'))
else:
    print(colored('[-] Pass error', 'red'))
    exit()

def up():
    proc = subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE)
    data = proc.stdout.read()
    print(data.rstrip().decode(str('866')))
    while True:
        name = input(colored('Choose file name>', 'yellow'))
        try:
            file = open(name, 'rb')
            break
        except FileNotFoundError:
            print(colored('[-] Error open file', 'red'))

    s.send(name.encode())
    data1 = s.recv(1).decode()
    try:
        if 2 in data1:
            print(colored('[-] Error', 'red'))
            return
    except:
        1
    while True:
        data = file.read(1024)
        if not(data):
            break
        s.send(data)
        s.recv(1)
    s.send('123\|/Done!'.encode())
    ask = s.recv(1).decode()
    if str(2) == ask:
        print(colored('[-] Error synchronization', 'red'))
        #print('Error synchronization. Ask: ' + str(ask))
    else:
        print(colored('[+] Done', 'green'))

s.send(str(1).encode())
while True:
    print(s.recv(3000).decode(str('866')))
    print(colored('1 - Download file', 'green'))
    print(colored('2 - Upload file', 'yellow'))
    print(colored('3 - Delete file', 'red'))
    cmd = int(input(colored('Choose>', 'yellow')))
    s.send(str(cmd).encode())
    s.recv(1)
    if cmd == 1:
        down()
    if cmd == 2:
        up()
    if cmd == 3:
        name = input(colored('Choose file name>', 'yellow'))
        s.send(name.encode())
        s.recv(1)
file.close()
s.close()
