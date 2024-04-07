import os
import threading
Shells = {}
Users = {}
cmdData = {}

class Shell:
    
    def __init__(self, name: str, id: str, title: None, inputtext, parametersSplitter):
        self.name = name
        self.id = id
        self.title = title
        self.commands = {}
        self.commandRestrictLevels = {}
        self.aliases = {}
        self.inputtext = inputtext
        self.init = False
        self.input = ""
        self.parametersSplitter = parametersSplitter
        global Shells
        Shells.update({self.name: self.id})

    def shellInput(self, user):
        if self.init:
            self.input = input(self.inputtext)
            inputSplit = self.input.split(" ")
            commandNameRaw = inputSplit[0]
            
            if commandNameRaw in self.aliases:
                commandName = self.aliases[commandNameRaw]
                
            else:
                commandName = commandNameRaw
            
            parameters = "".join(inputSplit[1:])
            parametersSplit = parameters.split(self.parametersSplitter)
            
            if commandName in self.commands:
                
                if commandName in self.commandRestrictLevels:
                    userProfile = user.getUserProfile()
                    
                    if self.commandRestrictLevels[commandName] <= userProfile:
                        self.commands[commandName](parameters=parametersSplit)  
                        
                    else:
                        print("Command Not Available")
                        
                else:
                    self.commands[commandName](parameters=parametersSplit)  
                    global cmdData
                    cmdData = {"Shell": self.name, "Command": commandName}
                    
            else:
                print("Command Not Available")
    
    def load(self):
        os.system("cls")
        self.init = True
        print(self.title)
        
        
    def addCommand(self, name, boundFunction):
        if name != "":
            self.commands.update({name: boundFunction})
            
        else:
            print("Command Name Can't Be Empty!")

    def removeCommand(self, name):
        if name in self.commands:
            del self.commands[name]
            
        else:
            print("Command Not Defined")
            
    def addAlias(self, target, name):
         if target in self.commands and name != "":
             self.aliases.update({name: target})
             
    def removeAlias(self, name):
        if name in self.aliases:
            del self.aliases[name]
            
        else:
            print("Alias Not Defined")
    
    def clear(self):
        os.system("cls")
    
    def resetCommands(self):
        self.commands = {}
        
    def resetAliases(self):
        self.aliases = {}
        
    def restrictCommand(self, target, level):
        self.commandRestrictLevels.update({target: level})
        
    def getCommands(self):
        return self.commands
    
    def getInfo(self):
        return {"shellName": self.name, "shellID": self.id, "shellCommands": self.commands, "restrictionLevels": self.commandRestrictLevels}
        
class User:
    
    def __init__(self, level):
        self.level = level
        
    def getUserProfile(self):
        return self.level
    
    def elevate(self, level):
        self.level = level
        
class Admin:
    
    def __init__(self):
        self.level = float("inf")
        
    def getUserProfile(self):
        return self.level

class Restricted:
    
    def __init__(self):
        self.level = float("-inf")
        
    def getUserProfile(self):
        return self.level
    
class SignedUser:
    
    def __init__(self, level):
        self.level = level
        
    def getUserProfile(self):
        return self.level

class Event:
    
    def __init__(self, listen, trigger):
        self.listen = listen
        self.trigger = trigger
    
    def listener(self):
        while True:
            if cmdData == self.listen:
                self.trigger()
                break
            
    def start(self):
        eventThread = threading.Thread(target=self.listener)
        eventThread.start()
        
class bundle:
    """In Case Of Commands With Same Name Across Different Shells, The Constructor Will Use The Command From The Shell With Higher Index."""
    
    def __init__(self, Shells):
        self.shells = Shells
        self.commands = {}
        temp = {}
        self.shellIdData = {}
        self.commandRestrictLevels = {}
        for i in Shells:
            temp = i.getInfo()
            self.commands.update({temp["shellID"]: temp["shellCommands"]})
            self.shellIdData.update({temp["shellID"]: i})
            self.commandRestrictLevels.update(temp["restrictionLevels"])
        
    def shellInput(self, user):
        if self.init:
            self.input = input(self.inputtext)
            inputSplit = self.input.split(" ")
            commandNameRaw = inputSplit[0]
            
            if commandNameRaw in self.aliases:
                commandName = self.aliases[commandNameRaw]
                
            else:
                commandName = commandNameRaw
            
            parameters = "".join(inputSplit[1:])
            parametersSplit = parameters.split(self.parametersSplitter)
            
            if commandName in self.commands:
                
                if commandName in self.commandRestrictLevels:
                    userProfile = user.getUserProfile()
                    
                    if self.commandRestrictLevels[commandName] <= userProfile:
                        self.commands[commandName](parameters=parametersSplit)  
                        
                    else:
                        print("Command Not Available")
                        
                else:
                    self.commands[commandName](parameters=parametersSplit)  
                    global cmdData
                    cmdData = {"Shell": self.name, "Command": commandName}
