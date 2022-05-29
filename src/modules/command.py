import sys
from tkinter import E
from typing import Dict, List, Callable

class Command:
    def __init__(self, handle:str):
        self.handle: str = handle
        self.description: str = handle + ' help'
        self.exec: Callable[[List[str]], None] = zero_args_command_function(self.help)
        self.argc: int = 0
        self.argv: List[str] = []
        self.sub_commands: Dict[str, Command] = {}
        self.flags: Dict[str,Callable] = {}
        self.shorts: Dict[str,str] = {}
        self.flag_has_parameter: Dict[str,bool] = {}
        self.shell_prefix: str = "> "

    def with_descryption(self, descrption):
        self.description = descrption
    
    def with_args(self, exec: Callable[[List[str]], None], argc: int):
        if len(self.sub_commands) != 0:
            raise Exception('Error: this command has sub operations, it can\'t also execute a function with arguments.')
        self.exec = exec
        self.argc = argc

    def with_no_args(self, exec: Callable[[], None]):
        self.exec = zero_args_command_function(exec)

    def with_sub_command(self, handle: str, sub_command):
        if handle in self.flags:
            raise Exception(f'Error: {handle} flag already exists.')
        if type(sub_command != Command):
            raise Exception('Error: type error sub_commant must be a Command object. ')
        if self.argc != 0:
            raise Exception('Error: this command has sub operations, it can\'t also execute a function with arguments.')
        sub_command.shell_prefix = ' ' + self.shell_prefix
        self.sub_commands[handle] = sub_command

    def with_flag(self, flag_handle: str, flag_short: str, flag_execute: Callable, takes_parameter: bool = False):
        if flag_handle in self.flags:
            raise Exception(f'Error: {flag_handle} flag already exists.')
        self.shorts[flag_short] = flag_handle
        self.flags[flag_handle] = flag_execute
        self.flag_has_parameter[flag_handle] = takes_parameter

    def help(self):
        print(self.helpstr)
    
    def set_argv(self, argv):
        self.argv = argv
    
    def run(self):
        self.argv = sys.argv
        if self.handle != self.parse_system_call():
            self.help()
            return
        try:
            self.parse()
        except Exception as _:
            self.help()


    def parse_system_call(self) -> str:
        return self.consume().split('/')[-1]
    
    def consume(self) -> str:
        argument = ''
        if len(self.argv) > 0:
            argument = self.argv[0]
            self.argv = self.argv[1:]
        return argument
        
    def parse(self):
        if self.super():
            if len(self.argv) == 0:
                self.shell()
                return
            sub_handle = self.consume()
            if sub_handle not in self.sub_commands:
                raise Exception('Error')
            sub_command = self.sub_commands[sub_handle]
            sub_command.set_argv(self.argv)
            sub_command.parse()
        else:
            if len(self.argv) < self.argc:
                raise Exception('Error')
            arguments = self.get_arguments()
            for argument in arguments:
                if self.is_flag(argument):
                    raise Exception('Error')
            self.parse_flags()
            self.exec(arguments)

    def super(self) -> bool:
        return len(self.sub_commands) != 0

    def shell(self):
        run_shell = True
        while(run_shell):
            self.argv  += input(self.shell_prefix).split(' ')
            if self.argv[0] == 'help':
                self.help()
                self.consume()
            elif self.argv[0] == 'quit' or self.argv[0] == 'exit':
                run_shell = False
                self.consume()
            else:
                try:
                    self.parse()
                except Exception as _ :
                    self.help()
                    self.consume()

    def get_arguments(self) -> List[str]:
        arguments = []
        for _ in range(self.argc):
            arguments.append(self.consume())
        return arguments
    
    def is_flag(self, argument:str) -> bool:
        return argument[0] == '-'
    
    def parse_flags(self):
        argument = self.consume()
        while(argument != ''):
            if not self.is_flag(argument):
                self.help()
                raise Exception('Error')
            if argument in self.shorts:
                argument = self.shorts[argument]
            if argument not in self.flags:
                self.help()
                raise Exception('Error')
            flag_exec = self.flags[argument]
            if self.flag_has_parameter[argument]:
                flag_exec(self.consume())
            flag_exec()



def zero_args_command_function(func: Callable[[], None]) -> Callable[[List[str]], None]:
    def new_func(_:List[str]):
        func()
    return new_func
