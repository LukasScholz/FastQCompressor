import unittest
from pathlib import Path

import FastQCompressor.FolderCompressor as FolderCompressor
import FastQCompressor.Config as Config

FOLDER = "test/data/testdatafolder"
CONFIG_PATH = "src/config/settings.xml"


class TestSubroutines(unittest.TestCase):
    def test_folder_compression(self):
        config = Config.Config(CONFIG_PATH)
        folder_extension = config.print(["FolderCompressor", "folderextension"])
        folder_compressor = FolderCompressor.FolderCompressor(CONFIG_PATH)
        folder_compressor.compress("test/data/testdatafolder", False)
        self.assertTrue(any(item.is_file() for item in Path(FOLDER).parent.glob("*" + folder_extension)))


if __name__ == "__main__":
    unittest.main()
