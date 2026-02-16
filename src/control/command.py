import shlex

class Command:
    commandType: str
    commandArgs: "list[str]"

    def __init__(
        self,
        commandString: str = None,
        commandType: str = None,
        commandArgs: "list[str]" = None,
    ) -> None:

        if commandType is not None and commandArgs is not None:
            self.commandType = commandType
            self.commandArgs = commandArgs
            return

        if commandString is not None:
            command_parts = shlex.split(commandString)
            self.commandType = command_parts[0]
            self.commandArgs = command_parts[1:]
            return
        
        self.commandType = "NoneCommand"
        self.commandArgs = []

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
    
    def __len__(self) -> int:
        return len(self.commandArgs)

    def get_command_type(self) -> str:
        return self.commandType

    def get_command_args(self) -> "list[str]":
        return self.commandArgs

    def get_command_arg(self, index: int) -> str:
        if index >= len(self.commandArgs) or index < 0:
            return None
        return self.commandArgs[index]

    
if __name__ == "__main__":
    command_str = input("Enter a command string to parse: ")

    command = Command(command_str)

    print(f"Command Type: {command.get_command_type()}")
    print("Command Args")

    for i in command.get_command_args():
        print(i)


