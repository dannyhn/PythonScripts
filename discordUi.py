import tkinter as tk
import tkinter.scrolledtext as tkst
import discordClient
import string
import time
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_login()
        self.localMaster = master
        self.channel = None
        self.server = None


    def create_login(self):
        self.entryEmail = tk.Entry(self, width = 30)
        self.entryEmail.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.entryPass = tk.Entry(self, show='*', width = 30)
        self.entryPass.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.button = tk.Button(self, width = 30)
        self.button["text"] = "Login"
        self.button["command"] = self.storeInfo
        self.button.pack()

    def storeInfo(self):
        self.email = self.entryEmail.get()
        self.password = self.entryPass.get()
        self.entryEmail.pack_forget()
        self.entryPass.pack_forget()
        self.button.pack_forget()
        self.create_widgets()

    def create_widgets(self):

        self.editTextString = tk.StringVar()

        self.text = tkst.ScrolledText(master=self, wrap = tk.WORD, width = 100, height = 40)
        self.text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text.config(state=tk.DISABLED)

        self.editText = tk.Entry(self, textvariable=self.editTextString, width=100)
        self.editText.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.localMaster.bind('<Return>', self.onEnterEvent)

        self.client = discordClient.Client(self.email, self.password)

        self.messageThread = threading.Thread(target=self.getMessageThread)
        self.messageThread.daemon = True
        self.messageThread.start()
        #self.test()

    def onEnterEvent(self, event):
        self.handleCommand(self.editTextString.get())
        #self.insertText(self.editTextString.get())
        self.editText.delete(0, tk.END)

    def insertText(self, msg):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.INSERT, "".join(filter(lambda x: x in string.printable, msg)) + "\n")
        self.text.config(state=tk.DISABLED)

    def handleCommand(self, command):
        if not command.startswith("/"):
            if self.channel != None:
                self.client.sendMessageToChannel(self.channel, command)
            return
        if command.startswith("/server"):
            self.handleServerCommand(command)
        if command.startswith("/channel"):
            self.handleChannelCommand(command)

    def handleServerCommand(self, command):
        splitCommand = command.split("/server ")
        if len(splitCommand) == 1: # get list of servers
            for name in self.client.getServerNames():
                self.insertText("Server: " + name)
        elif len(splitCommand) == 2:
            self.server = self.client.getServerByName(splitCommand[1])
            self.insertText("Connected to Server: " + self.server.getName())
            self.displayChannel()

    def handleChannelCommand(self, command):
        splitCommand = command.split("/channel ")
        if len(splitCommand) == 1: # get list of channels
            self.displayChannel()
        elif len(splitCommand) == 2:
            self.channel = self.client.getChannelByName(self.server, splitCommand[1])
            self.insertText("Connected to Channel: " + self.channel.getName())
            self.getMessages()

    def getMessages(self):
        if self.channel != None:
            print("Getting Messages")
            msgs = self.client.getMessagesFromChannel(self.channel)
            for msg in msgs:
                self.insertText("{:10} : {}".format(msg.name, msg.content))
        else:
            print("No Channel Set")

    def displayChannel(self):
        if self.server != None:
            for name in self.client.getChannelNames(self.server):
                self.insertText("Channel: " + name)

    def getMessageThread(self):
        while True:
            self.getMessages()
            time.sleep(20)


        
if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Danny's Client")
    app = Application(master=root)
    app.mainloop()