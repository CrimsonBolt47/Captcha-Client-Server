from email.mime import image
import tkinter as tk              
from tkinter import CENTER, LEFT, RAISED, SUNKEN, Button, Entry, Frame, IntVar, Label, StringVar, Variable,Radiobutton, font  as tkfont 
from PIL import ImageTk, Image
import socket
import threading
from time import sleep

class variable_holder(object):
    imgname = ""
    checkingname=""
    answerlist=[]
        
    @classmethod
    def getcaptchaname(cls,name):
        cls.imgname=name[:-4]
        print("got it",cls.imgname)
    @classmethod
    def getansname(cls,name):
        cls.checkingname=name
        print("got it",cls.checkingname)
    @classmethod
    def getanslst(cls,lst):
        cls.answerlist=lst
        print("got it",cls.answerlist)
    

class clientinterface:
    def __init__(self):
        print("client started")
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "192.168.135.1"
        self.ADDR = (self.SERVER,self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    
    def sendmessage(self,msg):
        message = msg.encode(self.FORMAT)
        msg_type= "message"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.1)
        self.client.send(message)
    
    def gettextcaptcha(self):
        msg_type="textcaptcha"
        img=open("temp.PNG",'wb')
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        sleep(0.1)
        imgsize=self.client.recv(1024)
        print("size",imgsize)
        imgdata=self.client.recv(int(imgsize))
        imgname=self.client.recv(1024).decode(self.FORMAT)
        variable_holder.getcaptchaname(imgname)
        img.write(imgdata)
    
    def getimagecaptcha(self):
        msg_type="imagecaptcha"
        send_type = str(msg_type).encode(self.FORMAT)
        self.client.send(send_type)
        img=[]
        for i in range(9):
            k=str(i)
            img.append(open("mm_%s.png" %k ,'wb'))
        correctanswer=self.client.recv(1024).decode(self.FORMAT)
        print("correct answer:-",correctanswer)
        answerlist=self.client.recv(1024).decode(self.FORMAT)
        print("answerlist",answerlist)
        for i in range(9):
            imgsize=self.client.recv(1024)
            print("size",imgsize)
            imgdata=self.client.recv(int(imgsize))
            img[i].write(imgdata)
        variable_holder.getansname(correctanswer)
        variable_holder.getanslst(answerlist.split(','))
        

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('500x400')
        self.title_font = tkfont.Font(family='Sans', size=18, weight="bold", slant="italic")
        container = tk.Frame(self,bg="Red")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, TextCaptcha,ImageCaptcha,Success):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    def updatecaptchatext(self,page_name):
        frame = self.frames[page_name]
        self.frames[page_name].updatecaptchatext()
    def updatecaptchaimage(self,page_name):
        frame = self.frames[page_name]
        self.frames[page_name].updatecaptchaimage()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.captchachoice=IntVar()
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(fill="x", pady=10)
        self.fram=tk.Frame(self,bg="RED")
        self.fram.pack(side="bottom")
        textcap = Radiobutton(self.fram, text="text captcha", variable=self.captchachoice, value=1)  
        textcap.pack()
        imagecap = Radiobutton(self.fram, text="image captcha", variable=self.captchachoice, value=2)  
        imagecap.pack()       
        button=Button(self,text="start",command=self.jumptochoice)
        button.pack()

    def jumptochoice(self):
        print(self.captchachoice.get())
        if(self.captchachoice.get()==1):
            clint.gettextcaptcha()
            self.controller.updatecaptchatext("TextCaptcha")
            self.controller.show_frame("TextCaptcha")
        else:
            clint.getimagecaptcha()
            self.controller.show_frame("ImageCaptcha")
            self.controller.updatecaptchaimage("ImageCaptcha")

        

class TextCaptcha(tk.Frame):

    def __init__(self, parent, controller):
        self.inpcaptcha=StringVar()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is Text captcha", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.frame = Frame(self, width=600, height=400)
        self.frame.pack()
        img1= ImageTk.PhotoImage(Image.open("starting.PNG"))
        self.cap=Label(self.frame,image=img1)
        self.cap.pack(side=LEFT)
        inp=Entry(self,textvariable=self.inpcaptcha)
        inp.pack()
        verify=Button(self,text="enter",command=self.verifytextcaptcha)
        verify.pack()
    def verifytextcaptcha(self):
        value=self.inpcaptcha.get()
        actualvalue=variable_holder.imgname
        print("enter value:-",value)
        print("actual value:-",actualvalue)
        if(value==actualvalue):
            self.controller.show_frame("Success")
    def updatecaptchatext(self):
        print("image updated")
        img = ImageTk.PhotoImage(Image.open("temp.PNG"))
        print(img)
        self.cap.configure(image=img)
        self.cap.image=img


class Success(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Success!!!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
class ImageCaptcha(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Find super in images", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        self.frame = Frame(self, width=600, height=400)
        self.frame.pack()
        img= ImageTk.PhotoImage(Image.open("super.png"))
        self.presed=[]
        self.cap=[]
        for i in range(9):
            self.cap.append(Button(self.frame,image=img,command= lambda c=i:self.savestate(c)))
            self.cap[i].grid(row=int(i/3),column=i%3,padx=2,pady=2)
            self.cap[i].image=img
            self.presed.append(False)
        self.check=Button(self,text="check",command=self.checkinput)
        self.check.pack()

    def updatecaptchaimage(self):
        self.label.config(text="find "+variable_holder.checkingname+" in images")
        for i in range(9):
            s=Image.open("mm_%s.png" %i)
            s=s.resize((120,120))
            img= ImageTk.PhotoImage(s)
            self.cap[i].config(image=img)
            self.cap[i].image=img
    def checkinput(self):
        iscorrect=True
        ans=variable_holder.answerlist
        print("answers in checkinput:-",ans)
        print("input status:-",self.presed)
        for i in range(9):
            if(str(i) not in ans):
                if(self.presed[i]==True):
                    iscorrect=False
            if(str(i) in ans):
                if(self.presed[i]==False):
                    iscorrect=False
        if(iscorrect==True):
            self.controller.show_frame("Success")

    def savestate(self,c):
        if(self.presed[c]==False):
            self.cap[c].config(relief=SUNKEN)
            self.presed[c]=True
        else:
            self.cap[c].config(relief=RAISED)
            self.presed[c]=False

if __name__ == "__main__":
    app = SampleApp()
    clint=clientinterface()
    app.mainloop()