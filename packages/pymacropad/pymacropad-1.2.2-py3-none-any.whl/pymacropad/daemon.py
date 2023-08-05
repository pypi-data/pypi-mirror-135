from enum import Enum
from time import sleep
from typing import Callable, List, Set

import libevdev
from os import path

from libevdev import InputEvent
from libevdev.device import DeviceGrabError


class KeyState(Enum):
    UP = 0
    DOWN = 1
    HELD = 2


class KeyEvent:
    @classmethod
    def from_event(cls, event: InputEvent, device_id: str):
        return cls(event.code.name, KeyState(event.value), device_id)

    def __init__(self, key: str, state: KeyState, device_id: str):
        self.key = key
        self.state = state
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
            try:
                if path.exists(self.device_path):
                    self._start_loop()
            except DeviceGrabError:
                pass
            print(f"Couldn't access {self.device_id}, waiting 5s...")
            sleep(5)


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
        key_event = KeyEvent.from_event(event, self.device_id)

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
