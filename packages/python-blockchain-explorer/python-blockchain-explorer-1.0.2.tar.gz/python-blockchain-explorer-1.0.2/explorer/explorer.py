import json
from importlib import resources

import requests

import explorer
from explorer import configs
from explorer.enums.fields_enum import FieldsEnum as fields
from explorer.utils.parsing import ResponseParser as parser


class BlockchainExplorer:
    def __new__(cls, api_key: str, net: str, prefix: str):
        with resources.path(configs, f"{net.upper()}-stable.json") as path:
            config_path = str(path)
        return cls.from_config(api_key=api_key, config_path=config_path, net=net, prefix=prefix)

    @staticmethod
    def __load_config(config_path: str) -> dict:
        with open(config_path, "r") as f:
            return json.load(f)

    @staticmethod
    def __run(func, api_key: str, net: str, prefix: str):
        def wrapper(*args, **kwargs):
            url = (
                f"{prefix.format(net.lower()).replace('-main','')}"
                f"{func(*args, **kwargs)}"
                f"{fields.API_KEY}"
                f"{api_key}"
            )
            r = requests.get(url, headers={"User-Agent": ""})
            return parser.parse(r)

        return wrapper

    @classmethod
    def from_config(cls, api_key: str, config_path: str, net: str, prefix: str):
        config = cls.__load_config(config_path)
        for func, v in config.items():
            if not func.startswith("_"):  # disabled if _
                attr = getattr(getattr(explorer, v["module"]), func)
                setattr(cls, func, cls.__run(attr, api_key, net, prefix))
        return cls


class Etherscan(BlockchainExplorer):
    def __new__(cls, api_key: str, net: str = "MAIN"):
        return BlockchainExplorer(api_key, net = "MAIN", prefix=fields.PREFIX)


class Arbiscan(BlockchainExplorer):
    def __new__(cls, api_key: str, net: str = "MAIN"):
        return BlockchainExplorer(api_key, net = "MAIN", prefix = "https://api.arbiscan.io/api?")
