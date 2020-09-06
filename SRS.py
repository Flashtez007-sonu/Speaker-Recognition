import sounddevice as sd
from scipy.io.wavfile import write
from tkinter import*
from trainingmodel import model
from testrecognition import result1
import tkinter.messagebox
from tkinter import ttk
from random import seed
import random
import time
import datetime
import os


def main():
    root = Tk()
    app = Window1(root)


class Window1:
    def __init__(self, master):
        self.master = master
        self.master.title("Speaker Recognition System")
        self.master.geometry('1350x750+0+0')
        self.master.config(bg ='powder blue')
        self.frame = Frame(self.master, bg ='powder blue')
        self.frame.pack()

        self.Username = StringVar()
        self.Password = StringVar()


        self.LabelTitle = Label(self.frame, text='SPEAKER RECOGNITION SYSTEM', font=('arial',50,'bold'),bd=20,)
        self.LabelTitle.grid(row=0,column=0,columnspan=2,pady=20)

        self.Loginframe1 = Frame(self.frame, width=1010, height=300,bd=20,relief='ridge')
        self.Loginframe1.grid(row=1, column=0)

        self.Loginframe2= Frame(self.frame, width=1000, height=100,bd=20,relief='ridge')
        self.Loginframe2.grid(row=2, column=0)

        self.Loginframe3= Frame(self.frame, width=1000, height=200,bd=20,relief='ridge')
        self.Loginframe3.grid(row=3, column=0,pady=2)
        #============================================================================================================================
        self.lbUsername = Label(self.Loginframe1, text='Username', font=('arial',30,'bold'),bd=22,)
        self.lbUsername.grid(row=0,column=0)
        self.txtUsername = Entry(self.Loginframe1, font=('arial',30,'bold'),bd=22,textvariable= self.Username)
        self.txtUsername.grid(row=0,column=1)

        self.lbPassword = Label(self.Loginframe1, text='Password', font=('arial',30,'bold'),bd=22,)
        self.lbPassword.grid(row=1,column=0)
        self.txtPassword = Entry(self.Loginframe1, font=('arial',30,'bold'),bd=22,textvariable= self.Password)
        self.txtPassword.grid(row=1,column=1, padx=85)
        #============================================================================================================================


        self.btnLogin = Button(self.Loginframe2,text='Login', width=20,font=('arial',17,'bold'),command = self.Login_System)
        self.btnLogin.grid(row=0, column=0)

        self.btnReset = Button(self.Loginframe2, text='Reset',width=20,font=('arial',17,'bold'),  command = self.Reset)
        self.btnReset.grid(row=0, column=1)

        self.btnExit = Button(self.Loginframe2, text='Exit', width=20,font=('arial',17,'bold'),command = self.iExit)
        self.btnExit.grid(row=0, column=2)
        
        #============================================================================================================================

        self.btnregister = Button(self.Loginframe3,text='Register', font=('arial',20,'bold'), command = self.register_window)
        self.btnregister.grid(row=0, column=0,pady=8,padx=20)
        
        self.btnenroll = Button(self.Loginframe3,text='Enrollment', font=('arial',20,'bold'),state=DISABLED, command = self.enroll_window)
        self.btnenroll.grid(row=0, column=1,pady=8,padx=20)

        self.btntest = Button(self.Loginframe3, text='Test', font=('arial',20,'bold'),state=DISABLED,command = self.test_window)
        self.btntest.grid(row=0, column=2,pady=8,padx=20)
        #============================================================================================================================

    def Login_System(self):
        global us
        global password
        user =(self.Username.get())
        pas = (self.Password.get())
        login=False

        files=os.listdir("users")
        for f in files:
            fname=f.split(".")[0]
            print(f.split(".")[0])
            if(fname ==  user):
                file=open("users/"+fname+".txt","r")
                file.readline()
                file.readline()
                ps=file.readline()
                ps.strip()
                print(ps)
                if(ps==pas):
                    login=True
                    us=user
                    password=pas
                    break

        if(login==True):
            self.btntest.config(state = NORMAL)
            self.btnenroll.config(state = NORMAL)
        else:
            tkinter.messagebox.askyesno("INVALID USER", "YOU ARE NOT A VALID USER, PLEASE REGISTER")
            self.btnenroll.config(state = DISABLED)
            self.btntest.config(state = DISABLED)
            self.Username.set("")
            self.Password.set("")
            self.txtUsername.focus()

    def Reset(self):
        self.btntest.config(state = DISABLED)
        self.Username.set("")
        self.Password.set("")
        self.txtUsername.focus()

    def iExit(self):
        self.iExit=tkinter.messagebox.askyesno("Exit", "Sure you want to Exit")
        if self.iExit > 0:
            self.master.destroy()
            return

        #============================================================================================================================

        
    def enroll_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window2(self.newWindow)

    def test_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window3(self.newWindow)

    def register_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window4(self.newWindow)   

class Window2:
    global cont
    cont = 0
    def __init__(self, master):
        self.master = master
        self.master.title("ENROLLMENT")
        self.master.geometry('1350x750+0+0')
        self.master.config(bg ='cadet blue')
        self.frame = Frame(self.master, bg ='powder blue')
        self.frame.pack()           

        #============================================================================================================================
        self.name = StringVar()
        

        self.lbname = Label(self.frame, text='Name', font=('arial',20,'bold'),bd=20,)
        self.lbname.grid(row=0,column=0)
        self.txtname = Entry(self.frame, font=('arial',22,'bold'),bd=20,textvariable= self.name)
        self.txtname.grid(row=0,column=1)
       
        self.record = Button(self.frame,text='record', font=('arial',20,'bold'),bd=20,command = self.start_record)
        self.record.grid(row=3, column=0,pady=10,padx=15)
        self.features = Button(self.frame,text='Features and Model', font=('arial',20,'bold'),bd=20,command=self.Features_Model)
        self.features.grid(row=3, column=1,pady=10,padx=15)
   
    def start_record(self):
        txtname = self.txtname.get()
        '''
        folder = "Speakers/"+txtname
        for filename in os.listdir(folder):
            file_path = os.path.join(folder,filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("failed to delete %s, REASON-- %s" % (file_path,e))
                '''
        print(txtname)
        #self.start_record=tkinter.messagebox.askyesno("RECORDING", "RECORDING IS STARTED")
        fs = 44100  # Sample rate
        print('recoding')
        seconds = 5  # Duration of recording
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        self.frame=tkinter.messagebox.askyesno("RECORDING", "RECORDING IS STARTED")
        sd.wait()  # Wait until recording is finished
        sd.stop()
        
        self.frame=tkinter.messagebox.askyesno("RECORDING", "RECORDING IS FINISHED")
        if os.path.exists('speakers/'):
            count =0
            value = random.randrange(0,10)
            parent_dir=('speakers/')
            print(value)
            
            path=os.path.join(parent_dir, txtname)
            if not os.path.exists(path):
                os.mkdir(path)
            if os.path.exists("speakers/"+txtname):
                write('speakers/'+txtname+'/'+txtname+str(value)+'.wav', fs, myrecording)# Save as WAV file 
                count = count+1    
        else:
            for txtname in os.path.exists("speakers/"):
                path=os.path.join(parent_dir, txtname)
                os.mkdir(path)
                write('speakers/'+txtname+'/'+txtname+str(value)+'.wav', fs, myrecording)
                count = count+1
                continue
            count = count+1
        print('Finished Recoding')
    def Features_Model(self):
        model()
               
            
            
        #============================================================================================================================



            
class Window3:
    def __init__(self, master):
        self.master = master
        self.master.title("TEST")
        self.master.geometry('1350x750+0+0')
        self.master.config(bg ='cadet blue')
        self.frame = Frame(self.master, bg ='powder blue')
        self.frame.pack()

       #============================================================================================================================
    
        self.name = StringVar()
        self.lbname = Label(self.frame, text='Name', font=('arial',20,'bold'),bd=20,)
        self.lbname.grid(row=0,column=0)
        self.txtname = Entry(self.frame, font=('arial',22,'bold'),bd=20,textvariable= self.name)
        self.txtname.grid(row=0,column=1)
        self.test = Button(self.frame,text='TEST YOUR AUDIO', font=('arial',20,'bold'),bd=20,command =self.start_record)
        self.test.grid(row=3, column=0,pady=10,padx=15)
        self.result = Button(self.frame,text='RESULT', font=('arial',20,'bold'),bd=20,command =self.result)
        self.result.grid(row=3, column=1,pady=10,padx=15)
        

  
    def result(self):
        result1()
        
        
        
    def start_record(self):
        txtname = self.txtname.get()
        fs = 44100  # Sample rate
        print('recoding')
        seconds = 5  # Duration of recording
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        self.frame=tkinter.messagebox.askyesno("RECORDING", "RECORDING IS STARTED")
        sd.wait()  # Wait until recording is finished
        sd.stop()
         
        self.frame=tkinter.messagebox.askyesno("RECORDING", "RECORDING IS FINISHED")
        if os.path.exists('voice/'):
            value = random.randrange(0,10)
            #count =0
            parent_dir=('voice/')
            #print(value)
             
            path=os.path.join(parent_dir, txtname)
            if not os.path.exists(path):
                os.mkdir(path)
            if os.path.exists("voice/"+txtname):
                 write('voice/'+txtname+'/'+txtname+str(value)+'.wav', fs, myrecording)# Save as WAV file
                 
                 
        else:
             for txtname in os.path.exists("voice/"):
                 path=os.path.join(parent_dir, txtname)
                 os.mkdir(path)
                 write('voice/'+txtname+'/'+txtname+'.wav', fs, myrecording)
                 continue
        print('Finished Recoding')      
         #test()
    
        


       #============================================================================================================================


class Window4:
    def __init__(self, master):
        self.master = master
        self.master.title("REGISTRATION")
        self.master.geometry('1350x750+0+0')
        self.master.config(bg ='cadet blue')
        self.frame = Frame(self.master, bg ='powder blue')
        self.frame.pack()
       #============================================================================================================================
        self.name = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        self.lbname = Label(self.frame, text='Name', font=('arial',20,'bold'),bd=20,)
        self.lbname.grid(row=0,column=0)
        self.txtname = Entry(self.frame, font=('arial',22,'bold'),bd=20,textvariable= self.name)
        self.txtname.grid(row=0,column=1)
        self.lbusername = Label(self.frame, text='Username', font=('arial',20,'bold'),bd=20)
        self.lbusername.grid(row=1,column=0)
        self.txtusername = Entry(self.frame, font=('arial',22,'bold'),bd=20,textvariable= self.username)
        self.txtusername.grid(row=1,column=1)
        self.lbpassword = Label(self.frame, text='Password', font=('arial',20,'bold'),bd=20)
        self.lbpassword.grid(row=2,column=0)
        self.txtpassword = Entry(self.frame, font=('arial',22,'bold'),bd=20,textvariable= self.password)
        self.txtpassword.grid(row=2,column=1)

        self.register = Button(self.frame,text='Register', font=('arial',20,'bold'),bd=20, command= self.register_user)
        self.register.grid(row=3, column=1,pady=10,padx=15)

    def register_user(self):
        name_info = self.txtname.get()
        username_info = self.txtusername.get()
        password_info = self.txtpassword.get()
        
   
        file=open("users/"+username_info+".txt","w")
        file.write(name_info+"\n")
        file.write(username_info+"\n")
        file.write(password_info)
        file.close()

        self.txtname.delete(0,END)
        self.txtusername.delete(0,END)
        self.txtpassword.delete(0,END)
            

       #============================================================================================================================

if __name__ == '__main__':
    root = Tk()
    app = Window1(root)
    root.mainloop()
    
