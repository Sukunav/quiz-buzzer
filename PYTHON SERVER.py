import pymysql
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

import sys

def sendmsg(message):
    text_output.insert(END,message+"\n")
    text_output.see(END)


# Set up the MySQL connection
def handle_client(client_socket):
        global reset
        request = client_socket.recv(1024).decode()
        sendmsg (request)
        
        # Example parsing the request, suppose we expect "SEND_QUIZ:<score>"
        if request.startswith("CHECK FOR RESET EXTRA:"):
            Sno = int(request.split(":")[1])
            reset=""
            db = pymysql.connect(
            host="localhost",
            user="root",
            password="IAMACODER78",
            database="quiz"
            )
            cursor=db.cursor()
            cursor.execute(f"SELECT reset_entry FROM quiz_entries WHERE Sno={Sno}")
            result = cursor.fetchall()
            for i in result:
                for j in i:
                    reset=j
            db.close()
            sendmsg (reset)
            # Send data back to ESP8266
            client_socket.send(str(reset).encode())
            sendmsg (f"{reset} msg sent")
            client_socket.close()
            sendmsg (f"closed connection from {addr}")

        elif request.startswith("CHECK FOR RESET:"):
            Sno = int(request.split(":")[1])
            reset=""
            while reset!="reset":
                db = pymysql.connect(
                host="localhost",
                user="root",
                password="IAMACODER78",
                database="quiz"
                )
                cursor=db.cursor()
                cursor.execute(f"SELECT reset_entry FROM quiz_entries WHERE Sno={Sno}")
                result = cursor.fetchall()
                for i in result:
                    for j in i:
                        reset=j
                db.close()
            sendmsg (reset)
            # Send data back to ESP8266
            client_socket.send(str(reset).encode())
            sendmsg ("reset msg sent")
            client_socket.close()
            sendmsg (f"closed connection from {addr}")
            
        
        elif request.startswith("SEND TO SERVER,"):
            db = pymysql.connect(
            host="localhost",
            user="root",
            password="IAMACODER78",
            database="quiz"
            )
            cursor=db.cursor()
            data=request.split(",")
            l2=[]
            for i in range(1,4):
                l2.append(data[i].strip())
            cursor.execute(f"INSERT INTO quiz_entries VALUES ({int(l2[0])}, \"{l2[1]}\",\"{l2[2]}\",\"\",{float(l2[3])})")
            sendmsg ("data inserted successfully")
            db.commit()
            db.close()
            client_socket.close()
            sendmsg (f"closed connection from {addr}")
        else:
            client_socket.close()

def start():
    try:
        global addr,server,text_output,running,client
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 8080))  # Replace with host IP and port if necessary
        server.listen(10)
        text_output=ScrolledText(win, wrap=WORD, width=80, height=20)
        text_output.place(x=50,y=100)
        sendmsg("Server is listening...")
        running=True

        while running:
            client, addr = server.accept()
            thread=threading.Thread(target=handle_client, args=(client,))
            thread.start()
            sendmsg(f"Accepted connection from {addr}")
    except OSError:
        print("OK")

def end():
    try:   
        global running
        running=False
        client.close()
        server.close()
        sendmsg("Server stopped")
        text_output.destroy()
    except OSError:
        print("OK")

def broadcast():
    local_ip = socket.gethostbyname(socket.gethostname())
    message = f"{local_ip}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.2)

    broadcast_ip = "255.255.255.255"  
    port = 12345                     
    print(f"Broadcasting IP: {message}")
    
    sock.sendto(message.encode(), (broadcast_ip, port))
    sock.close()
    start()

win=Tk()
win.geometry("800x600")
win.config(bg="orange")
StartServer=Button(win,text="START",font=("Arial",20),padx=10,pady=10,command=lambda: threading.Thread(target=start, daemon=True).start(),fg="red",bg="yellow")
StartServer.place(x=10,y=0)  
EndServer=Button(win,text="END",font=("Arial",20),padx=10,pady=10,command=lambda: end(),fg="white",bg="red")
EndServer.place(x=650,y=0)
BroadcastIP=Button(win,text="Broadcast IP",font=("Arial",20),padx=10,pady=10,command=lambda: threading.Thread(target=broadcast, daemon=True).start(),fg="red",bg="lime")
BroadcastIP.place(x=300,y=250)  

win.mainloop()