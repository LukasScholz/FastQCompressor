import unittest
import filecmp

import FastQCompressor.FastQ as FastQ

Files = ["test/data/HI.4019.002.index_7.ANN0831_R1.fastq", "test/data/HI.4019.002.index_7.ANN0831_R1.fastq.compressed",
         "test/data/HI.4019.002.index_7.ANN0831_R1.fastq.decompressed"]
CONFIG_PATH = "src/config/settings.xml"

class TestSubroutines(unittest.TestCase):

    def test_regular_file_decoding(self):
        filecompressor = FastQ.FileCompressor(CONFIG_PATH)
        filecompressor.compress(Files[0], Files[1])
        filecompressor.decompress(Files[1], Files[2])

        self.assertTrue(filecmp.cmp(Files[0], Files[2]))


if __name__ == '__main__':
    unittest.main()
