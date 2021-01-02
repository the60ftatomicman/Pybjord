import subprocess # import os -- in case subprocess fails
from time import (
    sleep
)
# Local
from virtual_keys import press
# 3rd Party
import win32gui # pip install pywin32
import re
import speech_recognition as sr

class WindowMgr:
    #set the wildcard string you will search for
    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self.window_enum_callback, wildcard)

    #enumurate through all the windows until you find the one you need
    def window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd ##pass back the id of the window

    #as a separate function, set the window to the foreground
    def set_foreground(self):
        win32gui.SetForegroundWindow(self._handle)
        win32gui.BringWindowToTop(self._handle)

def sendCommand(cmd):
    print("Received command [%s]" % cmd)
    if(cmd != '' and cmd != '/'and '/favicon.ico' not in cmd):
        formattedCmd = cmd.replace('/','',1).replace('/',' ').lower()
        print("Printing [%s]" % formattedCmd)
        press('enter_key') # hav to send sacrificial thingy first
        for ch in formattedCmd:
            if ch == ' ':
                press('spacebar')
            else:
                press(ch)
            sleep(0.01)
        sleep(1)
        press('enter_key')

if __name__ == '__main__':
    r = sr.Recognizer()
    mic = sr.Microphone()
    w = WindowMgr()
    with mic as source:
        while True:
            r.adjust_for_ambient_noise(source)
            print("Say something")
            audio = None
            try:
                audio = r.listen(source,10)
            except sr.WaitTimeoutError:
                print('Gotta reload, wait!')
                audio = None

                audio = None
            if audio != None:
                try:
                    cmd = r.recognize_google(audio)
                    print("I heard"+cmd)
                    w.find_window_wildcard(".*DOSBox*")
                    w.set_foreground()
                    sendCommand("/"+cmd)
                except sr.UnknownValueError:
                    print('What was that!')

