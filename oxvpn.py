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
    show_notifications(notifications.isChecked())
    auto_connect(autoconnect.isChecked())
    disable_ipv6(ipv6.isChecked())
    send_diagnostics(diagnostics.isChecked())
    force_dns(forcevpndns.isChecked())

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
def show_notifications(toggle):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set','desktop_notifications','on'])
    else:
        subprocess.run(['expressvpn','preferences','set','desktop_notifications','off'])

def disable_ipv6(toggle):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set','disable_ipv6','on'])
    else:
        subprocess.run(['expressvpn','preferences','set','disable_ipv6','off'])
def force_dns(toggle):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set','force_vpn_dns','on'])
    else:
        subprocess.run(['expressvpn','preferences','set','force_vpn_dns','off'])
def send_diagnostics(toggle):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set','send_diagnostics','on'])
    else:
        subprocess.run(['expressvpn','preferences','set','send_diagnostics','off'])
def auto_connect(toggle):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set','auto_connect','on'])
    else:
        subprocess.run(['expressvpn','preferences','set','auto_connect','off'])


#Start of the GUI

app = QApplication([])

# Configure the main window

mainwindow = QWidget()
#mainwindow.setGeometry(400,200,800,500)
mainwindow.setWindowTitle('OXvpn')

#Configure the layout

layout = QGridLayout()



serverlistbox = QListWidget()

disconnectbutton = QPushButton('Disconnect')
disconnectbutton.clicked.connect(lambda:disconnect())
connectbutton = QPushButton('Connect')
connectbutton.clicked.connect(lambda: chooseserver(codelist,serverlistbox.currentRow()))
statuslabel = QLabel(getstatus())
autoconnect = QCheckBox('Auto Connect')
networklockbox = QCheckBox('Network lock')
notifications = QCheckBox('Notifications')
ipv6 = QCheckBox('Disable ipv6')
forcevpndns = QCheckBox('Force vpn dns')
diagnostics = QCheckBox('Diagnostics')


networklockbox.setChecked(True)
print(networklockbox.isChecked())

serverlist = listservers()
layout.addWidget(serverlistbox,0,1,6,10)
layout.addWidget(autoconnect,0,0)
layout.addWidget(networklockbox,1,0)
layout.addWidget(notifications,2,0)
layout.addWidget(ipv6,3,0)
layout.addWidget(forcevpndns,4,0)
layout.addWidget(diagnostics,5,0)
layout.addWidget(disconnectbutton,7,1)
layout.addWidget(connectbutton,7,2)
layout.addWidget(statuslabel,8,0,1,11)

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
