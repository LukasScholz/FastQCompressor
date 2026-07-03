import xml.etree.ElementTree as Et
from idlelib.config import InvalidConfigType


class Config:
    def __init__(self, config_path):
        try:
            tree = Et.parse(config_path)
            self._root = tree.getroot()
        except FileNotFoundError:
            print("XML file not found!")
        except Et.ParseError:
            print("Invalid XML file!")
        # Todo: implement actual Exception handler

    def print(self, attribute_path):
            attribute = self._root
            for entry in attribute_path:
                attribute = attribute.find(entry)
                if attribute is None:
                    raise InvalidConfigType("Config Path not found!")
                    # Todo: implement actual Exception handler
            return attribute.text

    def get_all_children(self, attribute_path):
        attribute = self._root
        for entry in attribute_path:
            attribute = attribute.find(entry)
            if attribute is None:
                raise InvalidConfigType("Config Path not found!")
                # Todo: implement actual Exception handler
        return attribute.findall("./*")