class Command:
    commandType: str
    commandArgs: "list[str]"

    def __init__(self, commandString: str =None, commandType: str =None, commandArgs: "list[str]" =None) -> None:
        
        if commandType is not None and commandArgs is not None:
            self.commandType = commandType
            self.commandArgs = commandArgs
            return
        
        if commandString is not None:
            print("raw string: ", commandString)
            commandString = commandString.strip()
            commandParts: "list[str]" =[]
            lastCommandPartIndex: int = 0
            # Split the command string into a list of strings
            for i in enumerate(commandString, 0):
                print(i)
                if i[1] == " ":
                    commandParts.append(commandString[lastCommandPartIndex:i[0]])
                    lastCommandPartIndex = i[0]+1
                elif i[1] == "\"":
                    # Find the next quote
                    commandString.find("\"", i[0])
                    # Add the string to the list
                    commandParts.append(commandString[lastCommandPartIndex:i[0]+1])
                    lastCommandPartIndex = i[0]+1
                    
            commandParts.append(commandString[lastCommandPartIndex:])
            self.commandType = commandParts[0]
            self.commandArgs = commandParts[1:]
        pass

    def __str__(self) -> str:
        return self.commandType + " " + " ".join(self.commandArgs)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Command):
            return False
        return self.commandType == o.commandType and self.commandArgs == o.commandArgs
    
    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)
    
    def get_command_type(self) -> str:
        return self.commandType
    
    def get_command_args(self) -> "list[str]":
        return self.commandArgs
    
    def get_command_arg(self, index: int) -> str:
        if(index >= len(self.commandArgs)):
            return None
        return self.commandArgs[index]
    
    def get_command_arg_count(self) -> int:
        return len(self.commandArgs)
    


    
    