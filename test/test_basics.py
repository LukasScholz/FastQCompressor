from pathlib import Path
import unittest
from FastQCompressor.Config import Config

FILE_PATH = "src/config/testdata.xml"
file_config = Config(FILE_PATH)


class TestSubroutines(unittest.TestCase):
    def test_files(self):
        folder = file_config.print(["datafolder", "foldername"])
        files = file_config.get_all_children(["datafolder", "files"])
        all_found = True
        for file in files:
            if not Path(folder + "/" + file.find("filename").text).exists():
                all_found = False
        self.assertTrue(all_found)

    def test_file_not_found(self):
        with self.assertRaises(Config.ConfigException):
            Config("this/path/does/not/exist")

    def test_corrupted(self):
        folder = file_config.print(["datafolder", "foldername"])
        files = file_config.get_all_children(["datafolder", "files"])
        with self.assertRaises(Config.ConfigException):
            incorrect_file = folder + "/" + files[0].find("filename").text
            Config(incorrect_file)


if __name__ == "__main__":
    unittest.main()
