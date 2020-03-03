#!/usr/bin/env python3

import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication
import mainwindow
import subprocess

class Oxvpn(QtWidgets.QMainWindow, mainwindow.Ui_main_window):
    def __init__(self, parent=None):
        super(Oxvpn,self).__init__(parent)
        self.setupUi(self)
        self.auto_connect_box.setChecked(get_toggles('auto_connect'))
        self.network_lock_box.setChecked(get_toggles('network_lock'))
        self.notifications_box.setChecked(get_toggles('desktop_notifications'))
        self.ipv6_box.setChecked(get_toggles('disable_ipv6'))
        self.force_vpn_box.setChecked(get_toggles('force_vpn_dns'))
        self.diagnostics_box.setChecked(get_toggles('send_diagnostics'))
        self.serverlist = listservers()
        self.protocol_list = ['Auto','UDP','TCP']
        
        for i in self.protocol_list:
            self.protocol_combobox.addItem(i)
        
        self.codelist=[]
        for i in range(len(self.serverlist)-1):
            code = self.serverlist[i].split()
            self.codelist.append(code[0])
            location =""
            self.server_list_box.insertItem(i,location.join(code[1:]))
    
        self.connect_button.clicked.connect(lambda: self.chooseserver(self.codelist,self.server_list_box.currentRow()))
        self.disconnect_button.clicked.connect(lambda:self.disconnect())
        self.status_label.setText(getstatus())
        self.protocol_combobox.setCurrentIndex(self.get_protocol())

    def connect(self,server = 'smart'):
        self.disconnect()
        set_prefs(self.network_lock_box.isChecked(),'network_lock')
        set_prefs(self.notifications_box.isChecked(),'desktop_notifications')
        set_prefs(self.auto_connect_box.isChecked(),'auto_connect')
        set_prefs(self.ipv6_box.isChecked(),'disable_ipv6')
        set_prefs(self.diagnostics_box.isChecked(),'send_diagnostics')
        set_prefs(self.force_vpn_box.isChecked(),'force_vpn_dns')
        subprocess.run(['expressvpn','protocol',self.protocol_list[self.protocol_combobox.currentIndex()]])
        subprocess.run(['expressvpn','connect',server])
        self.status_label.setText(getstatus())

    def chooseserver(self,list,index):
        choice = list[index]
        self.connect(choice)

    def disconnect(self):
        subprocess.run(['expressvpn','disconnect'])
        self.status_label.setText(getstatus())
        
    def get_protocol(self):
        self.current_protocol = subprocess.run(['expressvpn','protocol'],capture_output=True,text=True)
        print(self.current_protocol.stdout)
        if self.current_protocol.stdout.strip() == 'auto':
            return 0
        elif self.current_protocol.stdout.strip() == 'udp':
            return 1
        elif self.current_protocol.stdout.strip() == 'tcp':
            return 2



def getstatus():
    status = subprocess.run(['expressvpn','status'],capture_output=True,text=True)
    statuslist = status.stdout.split()
    if statuslist[0] =='Not':
        return 'Not Connected'
        
    else:
        connection = ""
        print('Connected to ' + connection.join(statuslist[2:5]))
        return 'Connected to ' + connection.join(statuslist[2:5])




def listservers():
    servers = subprocess.run(['expressvpn','list','all'],capture_output=True,text=True)
    serverlist = servers.stdout.split('\n')
    del serverlist[0:3]
    del serverlist[-3:-1]
    return serverlist

def set_prefs(toggle,checkbox):
    if toggle == True:
        subprocess.run(['expressvpn','preferences','set',checkbox,'on'])
    else:
        subprocess.run(['expressvpn','preferences','set',checkbox,'off'])


def get_toggles(toggle):
    status = subprocess.run(['expressvpn','preferences',toggle],capture_output=True,text=True)
    if status.stdout.split()[0] == 'default' or status.stdout.split()[0] == 'true' :
        status = True
    else:
        status = False
    return status
   

def main():
    app = QApplication(sys.argv)
    window = Oxvpn()
    window.show()
    app.exec_()
    
        
if __name__ == '__main__':
    main()
