import configparser
import os


class CLI:
    def __init__(self):
        self._configfile = os.path.expanduser('~') + '/.fasttaskrc'
        self.config = configparser.ConfigParser()
        self.config.read(self._configfile)
        if(len(self.config.sections()) == 0):
            self.config.add_section('Settings')
            self.config.set('Settings', 'board', 'Default')
            self.config.set('Settings', 'max_work_session', '8')
            self.save_configs()
        self._board = self.config.get('Settings', 'board')
        self._max_work_session = int(self.config.get('Settings', 'max_work_session'))
            

    def main(self):
        print(self._configfile)

    def save_configs(self):
        with open(self._configfile, 'w') as configfile:
                self.config.write(configfile)
