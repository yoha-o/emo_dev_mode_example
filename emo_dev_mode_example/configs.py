import os
from dotenv import load_dotenv
import yaml


class EnvLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvLoader, cls).__new__(cls)
            cls._instance._load_env()
        return cls._instance

    def _load_env(self):
        load_dotenv(dotenv_path='.env')

    def get(self, key):
        return os.getenv(key)


class StringsLoader:
    _instance = None
    _strings_resource = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StringsLoader, cls).__new__(cls)
            cls._instance._load_strings()
        return cls._instance

    def _load_strings(self):
        with open('strings.yaml', encoding='utf-8') as f:
            self._strings_resource = yaml.safe_load(f)
