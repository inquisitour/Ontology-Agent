import configparser
import os
from typing import Any, Dict

class Config:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        self.config.read(config_path)

    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        return self.config.get(section, key, fallback=fallback)

    def getint(self, section: str, key: str, fallback: int = None) -> int:
        return self.config.getint(section, key, fallback=fallback)

    def getfloat(self, section: str, key: str, fallback: float = None) -> float:
        return self.config.getfloat(section, key, fallback=fallback)

    def getboolean(self, section: str, key: str, fallback: bool = None) -> bool:
        return self.config.getboolean(section, key, fallback=fallback)

    def get_section(self, section: str) -> Dict[str, str]:
        return dict(self.config[section]) if section in self.config else {}

def load_config(config_path: str = "config/ontology_agent.ini") -> Config:
    return Config(config_path)