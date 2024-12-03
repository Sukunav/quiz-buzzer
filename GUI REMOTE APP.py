from tkinter import *
from tkinter import ttk
import pymysql
import socket
host2=None
while host2==None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_port = 12345 
    sock.bind(("0.0.0.0", broadcast_port))  
    while True:
        data, addr = sock.recvfrom(1024)
        print("Starting your app in few secs")
        host2=str(data.decode())
        if host2!=None:
            sock.close()
            break

win=Tk()
win.geometry("1000x600")
win.config(bg="orange")
win.title("GUI REMOTE APP FOR QUIZ")
win.iconbitmap("speech-bubble.ico")

def add_pts(team):
    score=ptsEntry.get()
    connection=pymysql.connect(host=host2,user="root",password="IAMACODER78",database="quiz",port=3306)
    cursor=connection.cursor()
    query="SELECT MAX(Sno) FROM quiz_entries"
    cursor.execute(query) 
    result=cursor.fetchall()
    for i in result:
        for row in i:
            Sno=row
    query2=f"INSERT INTO {team}(quesno,score) VALUES ({Sno},{score})"
    cursor.execute(query2)
    connection.commit()
    connection.close()
    ptsEntry.delete(0,END)

def resetbtn():
    connection=pymysql.connect(host=host2,user="root",password="IAMACODER78",database="quiz",port=3306)
    cursor=connection.cursor()
    query="SELECT MAX(Sno) FROM quiz_entries"
    cursor.execute(query)
    result=cursor.fetchall()
    for i in result:
        for row in i:
            Sno=row
    query2=f"UPDATE quiz_entries SET reset_entry=\"reset\" WHERE Sno={Sno}"
    cursor.execute(query2)
    connection.commit()
    print ("reset inserted successfully")
    connection.close()

def show():
    global treev,scroll,frame
    frame=Frame(win)
    frame.place(x=200,y=300)

    connection=pymysql.connect(host=host2,user="root",password="IAMACODER78",database="quiz",port=3306)
    cursor=connection.cursor()
    query="SELECT MAX(Sno) FROM quiz_entries"
    cursor.execute(query)
    result1=cursor.fetchall()
    for i in result1:
        for row1 in i:
            Sno=row1
    query2=f"SELECT * FROM quiz_entries WHERE Sno={Sno}"
    cursor.execute(query2)
    result2=cursor.fetchall()
    connection.commit()
    treev=ttk.Treeview(frame,columns=("1","2","3","4","5"), show="headings",selectmode="browse")
    treev.pack(side="left")
    scroll=Scrollbar(frame,orient="vertical",command=treev.yview)
    scroll.pack(side="right",fill="y")
    treev.configure(yscrollcommand=scroll.set)
    treev.column("1",width=70,anchor="c")
    treev.column("2",width=70,anchor="c")
    treev.column("3",width=70,anchor="c")
    treev.column("4",width=70,anchor="c")
    treev.column("5",width=70,anchor="c")
    treev.heading("1",text="Ques no.")
    treev.heading("2",text="Team")
    treev.heading("3",text="Press status")
    treev.heading("4",text="Reset Entry")
    treev.heading("5",text="Timing")
    for i,row in enumerate(result2,start=1):
        treev.insert("","end",text=f"L{i}",values=row)
    connection.commit()
    connection.close()

def hide():
    treev.destroy()
    scroll.destroy()
    frame.destroy()

addpoints=Label(win,text="Add points to house",fg="yellow",bg="orange", font=("Arial",20))
addpoints.place(x=0,y=0)

pts=IntVar()

ptsEntry=Entry(win,textvariable=pts,bd=5)
ptsEntry.place(x=260,y=7)
ptsEntry.delete(0,END)


Agni=Label(win,text="Agni: ",fg="red",bg="orange", font=("Arial",24))
Agni.place(x=0,y=70)
Agnibut=Button(win,text="SUBMIT",fg="yellow",bg="red",font=("Arial",20),padx=10,pady=5,command=lambda: add_pts("agni"))
Agnibut.place(x=80,y=70)

Neer=Label(win,text="Neer: ",fg="cyan",bg="orange", font=("Arial",24))
Neer.place(x=230,y=70)
Neerbut=Button(win,text="SUBMIT",fg="yellow",bg="blue",font=("Arial",20),padx=10,pady=5,command=lambda: add_pts("neer"))
Neerbut.place(x=320,y=70)

Prithvi=Label(win,text="Prithvi: ",fg="lawn green",bg="orange", font=("Arial",24))
Prithvi.place(x=470,y=70)
Prithvibut=Button(win,text="SUBMIT",fg="red",bg="lawn green",font=("Arial",20),padx=10,pady=5,command=lambda: add_pts("prithvi"))
Prithvibut.place(x=580,y=70)

Vayu=Label(win,text="Vayu: ",fg="yellow",bg="orange", font=("Arial",24))
Vayu.place(x=730,y=70)
Vayubut=Button(win,text="SUBMIT",fg="red",bg="yellow",font=("Arial",20),padx=10,pady=5,command=lambda: add_pts("vayu"))
Vayubut.place(x=820,y=70)

reset=Button(win,command=lambda: resetbtn(),text="RESET",fg="yellow",bg="red",font=("Arial",20),padx=10,pady=10)
reset.place(x=425,y=155)

showbut=Button(win,text="SHOW",fg="red",bg="yellow",font=("Arial",20),padx=10,pady=5,command=lambda: show())
showbut.place(x=30,y=300)

hidebut=Button(win,text="HIDE",fg="red",bg="yellow",font=("Arial",20),padx=10,pady=5,command=lambda: hide())
hidebut.place(x=700,y=300)

win.mainloop()