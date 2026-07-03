from pathlib import Path
import unittest
from FastQCompressor.Config import Config
import xml.etree.ElementTree as Et

FILE_PATH = "src/config/testdata.xml"
file_config = Config(FILE_PATH)

class TestSubroutines(unittest.TestCase):

    def test_files(self):
        folder = file_config.print(["datafolder", "foldername"])
        files = file_config.get_all_children(["datafolder", "files"])
        all_found = True
        for file in files:
            if not Path(folder+"/"+file.find("filename").text).exists():
                all_found = False
        self.assertTrue(all_found)


if __name__ == '__main__':
    unittest.main()
