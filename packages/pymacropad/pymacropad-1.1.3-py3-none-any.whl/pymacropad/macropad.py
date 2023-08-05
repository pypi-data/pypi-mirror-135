from subprocess import Popen

from .config import Config
from .daemon import Daemon, KeyEvent


def start():
    config = Config(use_default=True)

    def handle(event: KeyEvent):
        command = config.get_command(event)
        if command is not None:
            Popen(command, shell=True)

    daemon = Daemon(config.device_id)
    daemon.handlers.add(handle)
    daemon.start()
