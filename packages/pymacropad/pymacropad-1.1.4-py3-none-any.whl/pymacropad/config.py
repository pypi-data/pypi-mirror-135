import os
from pathlib import Path
from shutil import copyfile
from typing import Dict, TypeVar

import yaml
from xdg import BaseDirectory

from pymacropad.daemon import KeyEvent, KeyState


class ConfigException(Exception):
    pass


class KeyConfig:
    def __init__(self, key: str, data: Dict[str, str] | str):
        self.key = key
        if type(data) == str:
            self.down = data
            self.held = None
            self.up = None
        else:
            self.down = data.get('down', None)
            self.held = data.get('held', None)
            self.up = data.get('up', None)

    def get_command(self, state: KeyState):
        if state == KeyState.DOWN:
            return self.down
        if state == KeyState.HELD:
            return self.held
        if state == KeyState.UP:
            return self.up
        return None

KC = TypeVar('KC', bound=KeyConfig)


class Config:
    _key_configs: Dict[str, KC] = {}
    _device_id: str
    _last_modified: float = None

    def __init__(self, config_file_name='pymacropad.yaml', use_default=False):
        self.config_file_name = config_file_name
        self.config_location = self._find_config() if not use_default else Config._default_config_path()
        print(f"Using config file at {self.config_location}")

    def get_command(self, event: KeyEvent):
        key_config = self.key_configs.get(event.key)
        if key_config is None:
            return
        return key_config.get_command(event.state)

    def _load(self):
        if os.path.getmtime(self.config_location) != self._last_modified:
            with open(self.config_location, 'r') as f:
                data = yaml.safe_load(f)
            self._last_modified = os.path.getmtime(self.config_location)

            self._key_configs = {k: self._build_key_config(k, v) for k, v in data.get('keys', {}).items()}
            self._device_id = data.get('device_id')

    @classmethod
    def _build_key_config(cls, key: str, data: dict) -> KC:
        return KeyConfig(key, data)

    @property
    def key_configs(self):
        self._load()
        return self._key_configs

    @property
    def device_id(self):
        self._load()
        return self._device_id

    def _find_config(self):
        config_base = Path(BaseDirectory.xdg_config_home)
        config_path = config_base.joinpath(self.config_file_name)
        if config_path.exists():
            return config_path
        return Config._create_config(config_path)

    @staticmethod
    def _create_config(config_location: Path):
        print(f"Creating default config file at {config_location}")
        copyfile(Config._default_config_path(), config_location)
        return config_location

    @staticmethod
    def _default_config_path():
        return Path(os.path.realpath(__file__)).parent.joinpath('default.yaml')
