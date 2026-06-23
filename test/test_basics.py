from pathlib import Path
import unittest

Files = ["test/data/HI.4019.002.index_7.ANN0831_R1.fastq"]

class TestSubroutines(unittest.TestCase):

    def test_files(self):
        all_found = True
        for file in Files:
            if not Path(file).exists():
                all_found = False
        self.assertTrue(all_found)


if __name__ == '__main__':
    unittest.main()
