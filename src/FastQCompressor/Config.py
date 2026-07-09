import xml.etree.ElementTree as Et


class Config:
    def __init__(self, config_path):
        try:
            tree = Et.parse(config_path)
            self._root = tree.getroot()
        except FileNotFoundError:
            raise self.ConfigException("FileNotFound", "Config file not found!", 404)
        except Et.ParseError:
            raise self.ConfigException("MalformedFile", "Invalid XML file!", 406)

    def print(self, attribute_path):
        attribute = self._root
        for entry in attribute_path:
            attribute = attribute.find(entry)
            if attribute is None:
                raise self.ConfigException("ValueNotFound", "Config value not found!", 404)
        return attribute.text

    def get_all_children(self, attribute_path):
        attribute = self._root
        for entry in attribute_path:
            attribute = attribute.find(entry)
            if attribute is None:
                raise self.ConfigException("ValueNotFound", "Config value not found!", 404)
        return attribute.findall("./*")

    class ConfigException(Exception):
        def __init__(self, exception_type: str, message: str, error_code: int):
            super().__init__(message)
            self.type = exception_type
            self.message = message
            self.error_code = error_code

        def __str__(self):
            return (f"{self.type} (Error Code: {self.error_code}) \n"
                    f"{self.message}")
