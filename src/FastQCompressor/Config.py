import xml.etree.ElementTree as Et


class Config:
    def __init__(self, config_path):
        """
        :param config_path: Path to the config file
        """
        try:
            tree = Et.parse(config_path)
            self._root = tree.getroot()
        except FileNotFoundError:
            raise self._ConfigException("FileNotFound", "Config file not found!", 404)
        except Et.ParseError:
            raise self._ConfigException("MalformedFile", "Invalid XML file!", 406)

    def print(self, attribute_path):
        """
        :param attribute_path: XML Path for the specific attribute
        :return: value of the attribute
        """
        attribute = self._root
        for entry in attribute_path:
            attribute = attribute.find(entry)
            if attribute is None:
                raise self._ConfigException("ValueNotFound", "Config value not found!", 404)
        return attribute.text

    def get_all_children(self, attribute_path):
        """
        :param attribute_path: XML Path for the specific attribute
        :return: all child config definitions below the specific attribute path
        """
        attribute = self._root
        for entry in attribute_path:
            attribute = attribute.find(entry)
            if attribute is None:
                raise self._ConfigException("ValueNotFound", "Config value not found!", 404)
        return attribute.findall("./*")

    class _ConfigException(Exception):
        def __init__(self, exception_type: str, message: str, error_code: int):
            """
            :param exception_type: Type of the Exceptions
            :param message: Error message containing specific information
            :param error_code: Associated HTML Error Code

            Exception Class for Config Related Exceptions
            """
            super().__init__(message)
            self.type = exception_type
            self.message = message
            self.error_code = error_code

        def __str__(self):
            return f"{self.type} (Error Code: {self.error_code}) \n{self.message}"
