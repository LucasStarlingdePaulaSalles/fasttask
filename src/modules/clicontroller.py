from src.modules.command import Command
from src.modules.cmd_example import example_cmd
import configparser
import os


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
        self.command = Command('fasttask').with_sub_command(example_cmd)

    def main(self):
        self.command.run()

    def save_configs(self):
        with open(self._config_file, 'w') as configfile:
                self.config.write(configfile)
