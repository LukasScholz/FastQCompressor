import os
import pickle
import FastQCompressor.SequenceMapper as SequenceMapper

FILEEXTENSION = ".compressed"

def compress(file, new_filename=None):
    fastq = _FastQ()
    if new_filename is None:
        new_filename = file+FILEEXTENSION # Default name
    fastq.compress_file(file, new_filename)

def decompress(file, new_filename=None):
    fastq = _FastQ()
    if new_filename is None:
        new_filename = os.path.splitext(file)[0]
    fastq.decompress_file(file, new_filename)

class _FastQ:
    def __init__(self):
        self.entries = []

    def save(self, new_filename):
        with open(new_filename, "wb") as file:
            pickle.dump(self.entries, file)

    def load(self, file):
        with open(file, "rb") as f:
            self.entries = pickle.load(f)

    def compress_file(self, file, new_filename):
        with open(file, "r") as file:
            remaining_lines = 0
            for line in file:
                # Sequence identifier
                if line.startswith("@"):
                    remaining_lines = 4

                match remaining_lines:

                    case 0:
                        # do not store info outside FastQ sequences
                        continue

                    case 4:
                        # line is identifier -> append new entry
                        self.entries.append([line])
                        remaining_lines -= 1

                    case 3:
                        # line is raw sequence
                        self.entries[-1].append(SequenceMapper.encode_sequence(line).save())
                        remaining_lines -= 1

                    case 2:
                        # line is descriptor sequence
                        self.entries[-1].append(line)
                        remaining_lines -= 1

                    case 1:
                        # line is quality sequence
                        self.entries[-1].append(SequenceMapper.encode_sequence(line).save())
                        remaining_lines -= 1

                    case _:
                        # something went horribly wrong
                        raise IOError("Malformatted FastQ File")
        self.save(new_filename)

    def decompress_file(self, file, new_filename):
        self.load(file)
        with open(new_filename, "w") as file:
            for entry in self.entries:
                file.write(entry[0]) # Sequence Identifier
                file.write(SequenceMapper.decode_sequence(entry[1])) # Raw Sequence
                file.write(entry[2]) # Descriptor Sequence
                file.write(SequenceMapper.decode_sequence(entry[3])) # Quality sequence
