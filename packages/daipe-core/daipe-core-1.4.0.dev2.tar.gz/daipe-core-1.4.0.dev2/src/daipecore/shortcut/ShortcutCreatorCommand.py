from argparse import Namespace, ArgumentParser
from daipecore.shortcut.ShortcutCreator import ShortcutCreator


class ShortcutCreatorCommand:
    def __init__(self, shortcut_creator: ShortcutCreator):
        self.__shortcut_creator = shortcut_creator

    def get_command(self) -> str:
        return "daipe:shortcuts:create"

    def get_description(self):
        return "Creates import shortcuts in src/daipe.py"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--path", dest="path", help="Path to create daipe.py at")

    def run(self, input_args: Namespace):
        self.__shortcut_creator.prepare_daipe_py(input_args.path)
