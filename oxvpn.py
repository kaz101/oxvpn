#!/usr/bin/env python3

import subprocess
import PyQt5 as q
from PyQt5.QtWidgets import  *


def disconnect():
    subprocess.run(['expressvpn','disconnect'])
    statuslabel.setText(getstatus())
    
def connect(server = 'smart'):
    disconnect()
    networklock(networklockbox.isChecked())
    subprocess.run(['expressvpn','connect',server])
    statuslabel.setText(getstatus())

def listservers():
    servers = subprocess.run(['expressvpn','list','all'],capture_output=True,text = True)
    serverlist = servers.stdout.split('\n')
    del serverlist[0:3]
    del serverlist[-3:-1]
    return serverlist

def chooseserver(list,index):
    choice = list[index]
    connect(choice)

def getstatus():
    status = subprocess.run(['expressvpn','status'],capture_output=True,text=True)
    statuslist = status.stdout.split()  
    if statuslist[0] =='Not':
        return 'Not Connected'
    else:
        connection = ""
        return 'Connected to ' + connection.join(statuslist[2:5])

def networklock(toggle):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set','network_lock','on'])
    else:
        subprocess.run(['expressvpn','preferences','set','network_lock','off'])   

#Start of the GUI

app = QApplication([])

# Configure the main window

mainwindow = QWidget()
mainwindow.setGeometry(400,200,800,500)
mainwindow.setWindowTitle('OXvpn')

#Configure the layout

layout = QVBoxLayout()



serverlistbox = QListWidget()

disconnectbutton = QPushButton('Disconnect')
disconnectbutton.clicked.connect(lambda:disconnect())
connectbutton = QPushButton('Connect')
connectbutton.clicked.connect(lambda: chooseserver(codelist,serverlistbox.currentRow()))
statuslabel = QLabel(getstatus())
networklockbox = QCheckBox('Network lock')
networklockbox.setChecked(True)
print(networklockbox.isChecked())

serverlist = listservers()

layout.addWidget(serverlistbox)
layout.addWidget(networklockbox)
layout.addWidget(disconnectbutton)
layout.addWidget(connectbutton)
layout.addWidget(statuslabel)

codelist=[]
for i in range(len(serverlist)-1):
    code = serverlist[i].split()
    codelist.append(code[0])
    location =""
    serverlistbox.insertItem(i,location.join(code[1:]))
    

selection = serverlistbox.selectedItems()
mainwindow.setLayout(layout)
mainwindow.show()





app.exec()
