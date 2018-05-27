import os


class Process:

    @staticmethod
    def home():
        return os.path.expanduser("~")

    @staticmethod
    def uname():
        return os.uname()[1]

    @staticmethod
    def has_package(package):
        return os.popen("command -v " + package).read() != ""

    @staticmethod
    def run(command: str):
        if command is not None and command != "":
            os.system(command)

    @staticmethod
    def run_if_has(package: str, command: str):
        if Process.has_package(package):
            Process.run(command)

    @staticmethod
    def run_with_message(package_manager, command: str, arguments: str, message: str):
        if package_manager is not None:
            if package_manager[command] != "":
                if message is not None and message != "":
                    print(message)
                Process.run(package_manager[command] + arguments)