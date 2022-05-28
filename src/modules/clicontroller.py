from ast import arguments
import configparser
from hashlib import new
from inspect import _void
import os
from re import sub
import sys
from tokenize import Number
from typing import Dict, List, Callable
from xmlrpc.client import boolean


class CLI:
    def __init__(self):
        self._config_file = os.path.expanduser('~') + '/.fasttaskrc'
        self.config = configparser.ConfigParser()
        self.config.read(self._config_file)
        if(len(self.config.sections()) == 0):
            self.config.add_section('Settings')
            self.config.set('Settings', 'board', 'Default')
            self.config.set('Settings', 'max_work_session', '8')
            self.save_configs()
        self._board = self.config.get('Settings', 'board')
        self._max_work_session = int(self.config.get('Settings', 'max_work_session'))
        self.command = Command('fasttask')
        self.command.sub_commands = {
            'board': Command('board'),
            'task': Command('task')
        }
            

    def main(self):
        self.command.run()

    def save_configs(self):
        with open(self._config_file, 'w') as configfile:
                self.config.write(configfile)

class Command:
    def __init__(self, handle:str):
        self.handle: str = handle
        self._help: str = handle + ' help'
        self.exec: Callable[[List[str]], None] = zero_args_command_function(self.help)
        self.argc: int = 0
        self.argv: List[str] = []
        self.sub_commands: Dict[str,Command] = {}
        self.flags: Dict[str,Callable] = {}
        self.shorts: Dict[str,str] = {}
        self.flag_has_parameter: Dict[str,boolean] = {}
        self.shell_prefix: str = "> "

    def help(self):
        print(self._help)
    
    def set_argv(self, argv):
        self.argv = argv
    
    def run(self):
        self.argv = sys.argv
        if self.handle != self.parse_system_call():
            self.help()
            return
        try:
            self.parse()
        except:
            self.help()


    def parse_system_call(self) -> str:
        return self.consume().split('/')[-1]

        
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


    def super(self) -> bool:
        return len(self.sub_commands) != 0
    
    def is_flag(self, argument:str) -> bool:
        return argument[0] == '-'

    def consume(self) -> str:
        argument = ''
        if len(self.argv) > 0:
            argument = self.argv[0]
            self.argv = self.argv[1:]
        return argument

    def get_arguments(self) -> List[str]:
        arguments = []
        for _ in range(self.argc):
            arguments.append(self.consume())
        return arguments



def zero_args_command_function(func: Callable[[], None]) -> Callable[[List[str]], None]:
    def new_func(_:List[str]):
        func()
    return new_func
