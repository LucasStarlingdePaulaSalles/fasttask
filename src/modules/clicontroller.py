from ast import arguments
import configparser
from hashlib import new
import os
import sys
from typing import List


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
            

    def main(self):
        print(self._config_file)

    def save_configs(self):
        with open(self._config_file, 'w') as configfile:
                self.config.write(configfile)

class Command:
    def __init__(self, handle:str):
        self.handle = handle
        self.help = handle + ' help'
        self.exec = self.help
        self.argc = 0
        self.argv = []
        self.sub_commands = {}
        self.flags = {}
        self.shorts = {}
        self.flag_has_parameter = {}
        self.shell_prefix = ""

    def help(self):
        print(self.help)
    
    def run(self):
        self.argv = sys.argv
        if self.handle != self.consume():
            self.help()
        self.parse()
        
    def parse(self):
        if self.super():
            if len(self.argv) == 0:
                self.shell()
            sub_handle = self.consume()
            if sub_handle not in self.sub_commands:
                self.help()
                return
            sub_command = self.sub_commands[sub_handle]
            sub_command.parse(self.argv)
        else:
            if len(self.argv) < self.argc:
                self.help()
                return
            arguments = self.consume(self.argc)
            for argument in arguments:
                if self.is_flag(argument):
                    self.help()
                    return
            
            
    
    def parse_flags(self):
        argument = self.consume()
        while(argument != ''):
            if not self.is_flag(argument):
                self.help()
                return
            if argument in self.shorts:
                argument = self.shorts[argument]
            if argument not in self.flags:
                self.help()
                return
            flag_exec = self.flags[argument]
            if self.flag_has_parameter[argument]:
                flag_exec(self.consume)
            flag_exec()


    def shell(self):
        pass

    def super(self) -> bool:
        return len(self.sub_commands) == 0
    
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




