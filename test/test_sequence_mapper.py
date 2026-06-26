import unittest

import FastQCompressor.SequenceMapper as SequenceMapper

Files = ["test/data/HI.4019.002.index_7.ANN0831_R1.fastq"]

class TestSubroutines(unittest.TestCase):

    def test_regular_sequence_decoding(self):
        text = "TACGCGGACTGCATGCGTGGTACGTCAGTCAGT"
        sequence_packer = SequenceMapper.encode_sequence(text)
        decoded = SequenceMapper.decode_sequence(sequence_packer.save())
        self.assertEqual(text, decoded)

    def test_single_char_sequence(self):
        text = "T"
        sequence_packer = SequenceMapper.encode_sequence(text)
        decoded = SequenceMapper.decode_sequence(sequence_packer.save())
        self.assertEqual(text, decoded)

    def test_zero_information_sequence(self):
        text = "GGGGGGGGGGGGGGGGGGGGGGGGG"
        sequence_packer = SequenceMapper.encode_sequence(text)
        decoded = SequenceMapper.decode_sequence(sequence_packer.save())
        self.assertEqual(text, decoded)

    def test_regular_length_reduction(self):
        text = "TACGCGGACTGCATGCGTGGTACGTCAGTCAGT"
        sequence_packer = SequenceMapper.encode_sequence(text)
        self.assertTrue(len(sequence_packer.sequence) < len(text))

if __name__ == '__main__':
    unittest.main()
