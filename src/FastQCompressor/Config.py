import xml.etree.ElementTree as Et
from idlelib.config import InvalidConfigType

CONFIG_PATH = "src/config/settings.xml"


class Config:
    def __init__(self):
        try:
            tree = Et.parse(CONFIG_PATH)
            self._settings = tree.getroot()
        except FileNotFoundError:
            print("XML file not found!")
        except Et.ParseError:
            print("Invalid XML file!")
        # Todo: implement actual Exception handler

    def get(self, attribute_path):
            attribute = self._settings
            for entry in attribute_path:
                attribute = attribute.find(entry)
                if attribute is None:
                    raise InvalidConfigType("Config Path not found!")
                    # Todo: implement actual Exception handler
            return attribute.text
