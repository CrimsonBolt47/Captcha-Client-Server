import socket 
import threading
from time import sleep
import os
import random
from random import randint
#server headers
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
parent_dir ="E:\\PYTHON_LAB_STUFF\\Projects\\Captcha Client Server\\Server"

def randomList(m, n):
    arr = [0] * m
    for i in range(n) :
        arr[randint(0, n) % m] += 1
    return arr
def mess(conn,addr):
    msg = conn.recv(1024).decode(FORMAT)
    if msg == DISCONNECT_MESSAGE:
        connected = False
    print(f"[{addr}] {msg}")

def sendtextcaptcha(conn,addr):
    num = random.randint(0,1070)
    print("random value:-",num)
    dir_list = os.listdir(parent_dir+"\\samples")
    print("random file chosen:-",dir_list[num])
    f=open(parent_dir+"\\samples\\"+dir_list[num],"rb")
    m=f.read()
    size=str(len(m)).encode(FORMAT)
    sleep(0.2)
    conn.send(size)
    sleep(0.2)
    conn.send(m)
    sleep(0.2)
    imgname=str(dir_list[num]).encode(FORMAT)
    conn.send(imgname)
    sleep(0.2)
    print("image sent")

def sendimagecaptcha(conn,addr):
    imageslist=["tiger","hydrant","bike"]
    corrctimage = random.randint(0,len(imageslist)-1)
    pics=[]
    for i,j in zip(range(3),imageslist):
        pics.append(os.listdir(parent_dir+"\\images\\"+j))
    numberofimageslst=randomList(3,9)
    print("number add:-",numberofimageslst)
    listofimagges=[]
    for i,n in zip(numberofimageslst,range(3)):
        print("first loop:-",i,n)
        for j in range(i):
            randimage=random.choices(pics[n])
            listofimagges.append(randimage)
    print("final images:-",listofimagges)
    newimagelist=[]
    for i in listofimagges:
        newimagelist.append(i[0])
    listofimagges=newimagelist
    random.shuffle(listofimagges)
    print("final final images:-",listofimagges)
    answerlist=[]
    for i,j in zip(listofimagges,range(9)):
        if(imageslist[corrctimage] in i):
            answerlist.append(j)
    print("answer:-",answerlist)
    sleep(0.2)
    corctans=str(imageslist[corrctimage]).encode(FORMAT)
    sleep(0.2)
    conn.send(corctans)
    ans=str(",".join(map(str,answerlist))).encode(FORMAT)
    sleep(0.2)
    conn.send(ans)
    sleep(0.2)
    for i in listofimagges:
        f=open(parent_dir+"\\images\\"+i[:-6]+"\\"+i,"rb")
        m=f.read()
        size=str(len(m)).encode(FORMAT)
        sleep(0.2)
        conn.send(size)
        sleep(0.2)
        conn.send(m)
        sleep(0.2)


        
def handle_client(conn, addr):
    i=0
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_type = conn.recv(HEADER).decode(FORMAT)
        if msg_type:
            print("type:-",msg_type)
            if(msg_type=="message"):
                mess(conn,addr)
            if(msg_type=="textcaptcha"):
                sendtextcaptcha(conn,addr)
            if(msg_type=="imagecaptcha"):
                sendimagecaptcha(conn,addr)
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()