import unittest
import FastQCompressor.SequenceMapper as SequenceMapper

CONFIG_PATH = "src/config/settings.xml"


class TestSubroutines(unittest.TestCase):
    def test_regular_sequence_decoding(self):
        sequencecoder = SequenceMapper.SequenceCoder(CONFIG_PATH)
        text = "TACGCGGACTGCATGCGTGGTACGTCAGTCAGT"
        sequence_packer = sequencecoder.encode_sequence(text)
        decoded = sequencecoder.decode_sequence(sequence_packer.save())
        self.assertEqual(text, decoded)

    def test_single_char_sequence(self):
        sequencecoder = SequenceMapper.SequenceCoder(CONFIG_PATH)
        text = "T"
        sequence_packer = sequencecoder.encode_sequence(text)
        decoded = sequencecoder.decode_sequence(sequence_packer.save())
        self.assertEqual(text, decoded)

    def test_zero_information_sequence(self):
        sequencecoder = SequenceMapper.SequenceCoder(CONFIG_PATH)
        text = "GGGGGGGGGGGGGGGGGGGGGGGGG"
        sequence_packer = sequencecoder.encode_sequence(text)
        decoded = sequencecoder.decode_sequence(sequence_packer.save())
        self.assertEqual(text, decoded)

    def test_regular_length_reduction(self):
        sequencecoder = SequenceMapper.SequenceCoder(CONFIG_PATH)
        text = "TACGCGGACTGCATGCGTGGTACGTCAGTCAGT"
        sequence_packer = sequencecoder.encode_sequence(text)
        self.assertTrue(len(sequence_packer.sequence) < len(text))


if __name__ == "__main__":
    unittest.main()
