import configparser
import os
from typing import List

from src.modules.cmd_example import example_cmd
from src.modules.command import Command
from src.modules.dbhandler import DBHandler


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
        self._max_work_session = int(
            self.config.get('Settings', 'max_work_session'))
        self.dbh = DBHandler()
        self.board = self.dbh.get_board(self._board)

    def main(self):
        board_create_cmd = Command("create").with_args(self.board_create(), 2)
        board_list_cmd = Command("list").with_no_args(self.board_list())
        board_checkout_cmd = Command(
            "checkout").with_args(self.board_checkout(), 1)
        board_delete_cmd = Command("delete").with_args(self.board_delete(), 1)
        board_cmd = Command("board") \
            .with_sub_command(board_create_cmd) \
            .with_sub_command(board_list_cmd) \
            .with_sub_command(board_checkout_cmd) \
            .with_sub_command(board_delete_cmd)
        self.command = Command('fasttask').with_sub_command(board_cmd)

        self.command.run()

    def board_create(self):
        def board_create_cmd(data: List[str]) -> None:
            id = self.dbh.create_board(data[0], data[1])
            self.board = self.dbh.get_board(id)

        return board_create_cmd

    def board_list(self):
        def board_list_cmd() -> None:
            return self.dbh.get_boards

        return board_list_cmd

    def board_checkout(self):
        def board_checkout_cmd(data: List[str]) -> None:
            self.board = self.dbh.get_board(int(data[0]))

        return board_checkout_cmd

    def board_delete(self):
        def board_delete_cmd(data: List[str]) -> None:
            board_id = int(data[0])
            if self.board.get_board_id() != board_id:
                self.dbh.delete_board(board_id)

        return board_delete_cmd

    def save_configs(self):
        with open(self._config_file, 'w') as configfile:
            self.config.write(configfile)
