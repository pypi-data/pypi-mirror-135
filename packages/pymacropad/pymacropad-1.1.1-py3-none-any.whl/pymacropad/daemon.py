from enum import Enum
from typing import Callable, List, Set

import libevdev
from evdev import InputDevice, ecodes
from select import select
from subprocess import Popen
from os import path
from time import sleep

from libevdev import InputEvent


class KeyState(Enum):
    UP = 0
    DOWN = 1
    HELD = 2


class KeyEvent:
    def __init__(self, event: InputEvent, device_id: str):
        self.key = event.code.name
        self.state: KeyState = KeyState(event.value)
        self.device_id = device_id


class Daemon:
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.handlers: Set[Callable[[KeyEvent], None]] = set()

    @property
    def device_path(self):
        return f'/dev/input/by-id/{self.device_id}'

    def start(self):
        while True:
            if path.exists(self.device_path):
                self._start_loop()


    def _start_loop(self):
        with open(self.device_path, 'rb') as fd:
            device = libevdev.Device(fd)
            device.grab()
            print("Device connected")

            while True:
                for event in device.events():
                    if not event.matches(libevdev.EV_KEY):
                        continue
                    self._handle(event)

    def _handle(self, event: InputEvent):
        key_event = KeyEvent(event, self.device_id)
        print(f"Handling key: {key_event.key}, state: {key_event.state}")

        for handler in self.handlers:
            handler(key_event)



if __name__ == '__main__':
    d = Daemon('usb-CapsUnlocked_CU7-event-kbd')
    d.start()



# class Daemon:
#     def __init__(self, config: Config):
#         self.config = config
#
#     def start(self):
#         while True:
#             if path.exists(self.config.device):
#                 self.handle_loop()
#             else:
#                 sleep(3)
#
#     def handle_loop(self):
#         try:
#             dev = InputDevice(self.config.device)
#             print("device connected")
#
#             with dev.grab_context():
#                 while True:
#                     select([dev], [], [])
#                     for event in dev.read():
#                         if event.type == ecodes.EV_KEY:
#                             self.handle(event.code, event.value)
#         except OSError as e:
#             print("device disconnected", e)
#
#     def handle(self, code, state):
#         key, mod = constants.SHIFT_MAP[code]
#         state = constants.STATE_MAP[state]
#         print(f"handling key: {key}, mod: {mod}, state: {state}")
#         conf = self.config.key_configs.get(key)
#         if conf is None:
#             return
#         command = conf.get_command(state, mod)
#         if command is None:
#             return
#         print(f"\texecuting: {command}")
#         Popen(command, shell=True)
#
#
# def start():
#     config = Config()
#     daemon = Daemon(config)
#     daemon.start()
