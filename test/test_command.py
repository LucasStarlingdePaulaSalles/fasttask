import unittest
from typing import List
from fasttask.modules.command import Command

class TestCommand(unittest.TestCase):

    def test_command_with_subcommand_cannot_have_args(self):
        def any_function(_: List[str]) -> None:
            return None

        with self.assertRaises(Exception) as exception:
            new_command = Command('test_command')
            sub_command = Command('test_sub_command')
            new_command.with_sub_command(sub_command)
            new_command.with_args(any_function, 1)

    def test_command_with_args_cannot_have_subcommands(self):
        def any_function(_: List[str]) -> None:
            return None

        with self.assertRaises(Exception) as exception:
            new_command = Command('test_command')
            sub_command = Command('test_sub_command')

            new_command.with_args(any_function, 1)
            new_command.with_sub_command(sub_command)

    def test_subcommand_must_be_a_command(self):
        with self.assertRaises(Exception) as exception:
            new_command = Command('test_command')
            sub_command = lambda x: x + 2

            new_command.with_sub_command(sub_command)

    def test_subcommand_must_be_unique(self):
        with self.assertRaises(Exception) as exception:
            new_command = Command('test_command')

            sub_command = Command('test_sub_command')
            new_command.with_sub_command(sub_command)
            new_command.with_sub_command(sub_command)

    def test_command_flag_must_be_unique(self):
        def none_function():
            return None

        with self.assertRaises(Exception) as exception:
            new_command = Command('test_command')
            new_command.with_flag('teste', 'ts', none_function)
            new_command.with_flag('teste', 'ts', none_function)

    def test_flags_are_properly_sanitized(self):
        def none_function():
            return None

        new_command = Command('test_command')
        new_command.with_flag('teste', 'ts', none_function)

        self.assertEqual(new_command.sanitize_flags('--teste'), '--teste')
