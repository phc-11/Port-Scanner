import socket
import threading
from queue import Queue

target = "192.168.0.1"
myQueue = Queue()
openPorts = []


def portScan(port):
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((target, port))
        return True
    except:
        return False
    

def fillQueue(ports):
    for port in ports:
        myQueue.put(port)


def exec():
    while not myQueue.empty():
        port = myQueue.get()
        if portScan(port):
            print("Port {} is open!".format(port))
            openPorts.append(port)

ports = range(1,5000)
fillQueue(ports)

threadList = []


for t in range(1024):
    thread = threading.Thread(target=exec)
    threadList.append(thread)

for thread in threadList:
    thread.start()

for thread in threadList:
    thread.join()

print("Open ports are: ", openPorts)
