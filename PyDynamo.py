import os
import threading
from colorama import Fore as Colors

colors = {
    "BLACK": Colors.BLACK,
    "RED": Colors.RED,
    "GREEN": Colors.GREEN,
    "YELLOW": Colors.YELLOW,
    "BLUE": Colors.BLUE,
    "MAGENTA": Colors.MAGENTA,
    "CYAN": Colors.CYAN,
    "WHITE": Colors.WHITE,
    "RESET": Colors.RESET,
    "LIGHTBLACK_EX": Colors.LIGHTBLACK_EX,
    "LIGHTRED_EX": Colors.LIGHTRED_EX,
    "LIGHTGREEN_EX": Colors.LIGHTGREEN_EX,
    "LIGHTYELLOW_EX": Colors.LIGHTYELLOW_EX,
    "LIGHTBLUE_EX": Colors.LIGHTBLUE_EX,
    "LIGHTMAGENTA_EX": Colors.LIGHTMAGENTA_EX,
    "LIGHTCYAN_EX": Colors.LIGHTCYAN_EX,
    "LIGHTWHITE_EX": Colors.LIGHTWHITE_EX
}



Users = {}
cmdData = {}

class User:
    
    def __init__(self, level: int):

        self.level = level
        
    def getUserProfile(self):

        return self.level
    
    def setUserLevel(self, level: int):

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
    
    def __init__(self, level: int):

        self.level = level
        
    def getUserProfile(self):

        return self.level

class Event:
    
    def __init__(self, listen: dict, trigger: function):

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

class Theme:
    
    def __init__(self, inputTextCharacter: str, inputTextCharacterColor, userInputColor, outputColor, errorColor, titleColor, parameterSplitter: str):

        self.inputText = inputTextCharacter
        self.parameterSplitter = parameterSplitter
        self.colors = {
            "input text": inputTextCharacterColor,
            "user input": userInputColor,
            "output": outputColor,
            "error": errorColor,
            "title": titleColor
        }

    def getTheme(self):

        return [self.parameterSplitter, self.inputText, self.colors]
    


class Shell:
    
    def __init__(self, name: str, title: None, theme: Theme):

        self.name = name
        self.title = title 

        self.commands = {
            "cls": self.clear

        }

        self.commandRestrictLevels = {}

        self.aliases = {
            "clear": "cls"

            }
        
        self.theme = theme.getTheme()

        self.inputtext = self.theme[1]
        self.init = False

        self.input = "" 
        self.parametersSplitter = self.theme[0]
        self.themeColors = self.theme[2]

    def shellInput(self, user):

        if self.init:

            self.input = input(self.themeColors["input text"] + self.inputtext + self.themeColors["user input"])
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

                        print(self.themeColors["error"], "Command Not Available", Colors.WHITE)
                        
                else:

                    self.commands[commandName](parameters=parametersSplit)  
                    global cmdData
                    cmdData = {"Shell": self.name, "Command": commandName}
                    
            else:

                print(self.themeColors["error"], "Command Not Available", Colors.WHITE)
    
    def load(self):

        os.system("cls")
        self.init = True
        print(self.themeColors["title"], self.title, Colors.WHITE)
        
        
    def addCommand(self, name: str, boundFunction: function):

        if name != "":

            self.commands.update({name: boundFunction})
            
        else:

            print(self.themeColors["error"], "Command Name Can't Be Empty!", Colors.WHITE)

    def removeCommand(self, name: str):

        if name in self.commands:
            
            del self.commands[name]
            
        else:

            print(self.themeColors["error"], "Command Not Defined", Colors.WHITE)
            
    def addAlias(self, target: str, name: str):
         
         if target in self.commands and name != "":
             
             self.aliases.update({name: target})
             
    def removeAlias(self, name: str):

        if name in self.aliases:

            del self.aliases[name]
            
        else:

            print(self.themeColors["error"], "Alias Not Defined", Colors.WHITE)
    
    def clear(self, parameters: list):

        os.system("cls")
        print(self.themeColors["title"], self.title, Colors.WHITE)
    
    def resetCommands(self):

        self.commands = {}
        
    def resetAliases(self):

        self.aliases = {}
        
    def restrictCommand(self, target: str, level: int):

        if target in self.commands:
            self.commandRestrictLevels.update({target: level})

        else:
            
            return "INVALID COMMAND"
        
        
    def getCommands(self):

        return self.commands
    
    def getInfo(self):

        return {"shellName": self.name, "shellID": self.id, "shellCommands": self.commands, "restrictionLevels": self.commandRestrictLevels}
    
    def print(self, text: str):

        print(self.themeColors["output"], text, Colors.WHITE)

    def setTheme(self, theme: Theme, refresh: bool):

        self.theme = Theme.getTheme()

        self.inputtext = self.theme[1]
        self.parametersSplitter = self.theme[0]
        self.themeColors = self.theme[2]

        if refresh:

            self.clear()

class Var:

    def __init__(self, data, id: str):

        self.data = data
        self.id = id

class Env:

    def __init__(self, id: str):
        
        self.id = id
        self.var = {}

    def addVar(self, var: Var):

        self.var.update({var.id: var})

    def getVar(self, id: str):

        try:
            
            return self.var[id].data
        
        except:

            print("Invalid Variable ID!")

# Default Environments

version = Var(["RELEASE", "2.0", "FEATURE"], "version")

VersionData = Env("VersionData")
VersionData.addVar(version)

        
# Default Functions

def getVersion():

    data = VersionData.getVar("version")
    return f"{data[0]} {data[1]} ( {data[2]} )"

def generateThemeFromDict(data: dict):

    try:

        return Theme(data["input text character"], data["colors"]["input text"], data["colors"]["user input"], data["colors"]["output"], data["colors"]["error"], data["colors"]["title"], data["parameter splitter"])

    except:

        print("Invalid Theme!")

# Default Themes

DEFAULTTHEME1 = Theme("   >>> ", Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, " ")
DEFAULTTHEME2 = Theme("   >>> ", Colors.WHITE, Colors.LIGHTYELLOW_EX, Colors.WHITE, Colors.RED, Colors.WHITE, " ")
DEFAULTTHEME3 = Theme("   >>> ", Colors.WHITE, Colors.LIGHTYELLOW_EX, Colors.LIGHTGREEN_EX, Colors.RED, Colors.WHITE, " ")
DEFAULTTHEME4 = Theme("   >>> ", Colors.WHITE, Colors.LIGHTGREEN_EX, Colors.LIGHTYELLOW_EX, Colors.RED, Colors.WHITE, " ")
DEFAULTTHEME5 = Theme("   >>> ", Colors.RED, Colors.LIGHTGREEN_EX, Colors.LIGHTYELLOW_EX, Colors.RED, Colors.WHITE, " ")

# Default Shell

DEFAULTSHELL = Shell("Default Shell", "DEFAULT SHELL", DEFAULTTHEME1)

def execute(parameters):

    os.system(input("ENTER COMMAND: "))
        

DEFAULTSHELL.addCommand("exec", execute)