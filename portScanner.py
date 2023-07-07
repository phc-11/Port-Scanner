import sys
import socket
import threading
from queue import Queue

#Establish the target of the PortScanner from standard input

#Try statement to attempt to read the target address from standard input, in the case of a failure to read input program will exit gracefully
try:

    #Reading input from standard input and storing the string in target
    target = input("Enter the target IP address you would like to scan: ")
except:
    print("Invalid input")
    sys.exit(1)

try:
    portBottom,portTop = input("Please enter the range of ports you would like to scan (Ex: 1 5000 will scan ports 1-5000)").split()
except:
    print("Invalid port range")
    sys.exit(1)



#Declare our Queue that will be used 
myQueue = Queue()

#Declare our array of open ports that will be used to print the open ports on the target address
openPorts = []

#Our function that scans for open ports
def portScan(port):

    #Using a try and except method to return True or False depending if the port is open
    try:

        #Establishing our socket (AF_INET is declaring this as an internet socket, SOCK_STREAM is for TCP connections)
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Attempting to connect to our target port
        mySocket.connect((target, port))

        #Returns True if the port is avaliable
        return True
    
    except:

        #Returns False if the port is unavaliable
        return False
    
#Function that fills our Queue with the range of ports (In this case 1-5000)
def fillQueue(ports):

    #For loop to iterate from 0 to the last index of ports
    for port in ports:

        #Put the iteration of ports in the queue
        myQueue.put(port)

#Function that will act as our "driver", this function will be multithreaded to execute port scanning at a faster rate
def exec():

    #While loop that will continue to loop until the queue is empty
    while not myQueue.empty():

        #Pop the next port number from the queue
        port = myQueue.get()

        #Will check to see if the port is avaliable, if true will print and append the port number to our array of avaliable ports
        if portScan(port):

            #Print the avaliable port to standard output
            print("Port {} is open!".format(port))

            #Adds the port to the end of our array of avaliable ports
            openPorts.append(port)

#Establishes the range of ports we want to check
ports = range(int(portBottom),int(portTop))

#Calls fillQueue to fill our queue with the designated range of ports
fillQueue(ports)

#Establishing an array that will hold our threaded processes
threadList = []

#For loop that will create our desired amount of threads (in this case 1024)
for t in range(1024):

    #Establish this thread, and set it to execute the function exec
    thread = threading.Thread(target=exec)

    #Add this function to our array of threads
    threadList.append(thread)

#For loop to start our threaded processes
for thread in threadList:
    thread.start()

#For loop that prevents the calling thread until the thread that is calling .join() is complete, this prevents indefinite hangs or zombie processes
for thread in threadList:
    thread.join()

#Prints all of the avaliable ports in one line
print("Open ports are: ", openPorts)
