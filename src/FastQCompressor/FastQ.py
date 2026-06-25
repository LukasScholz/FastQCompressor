import ast
import os
import FastQCompressor.SequenceMapper as SequenceMapper

FILEEXTENSION = ".compressed"

def compress(file, new_filename=None):
    fastq = _FastQ()
    if new_filename is None:
        new_filename = file+FILEEXTENSION # Default name
    fastq.compress_file(file)
    fastq.print_entries(new_filename)

def decompress(file, new_filename=None):
    fastq = _FastQ()
    if new_filename is None:
        new_filename = os.path.splitext(file)[0]
    result = fastq.decompress_file(file)
    with open(new_filename, "w") as file:
        file.write(result)

class _FastQ:
    def __init__(self):
        self.entries = []

    def print_entries(self, new_filename):
        with open(new_filename, "w") as file:
            for entry in self.entries:
                for line in entry:
                    file.write(line+"\n")

    def compress_file(self, file):
        with open(file, "r") as file:
            remaining_lines = 0
            for line in file:
                line = line.replace("\n","")
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
                        self.entries[-1].append(SequenceMapper.encode_sequence(line).__str__())
                        remaining_lines -= 1

                    case 2:
                        # line is descriptor sequence
                        self.entries[-1].append(line)
                        remaining_lines -= 1

                    case 1:
                        # line is quality sequence
                        self.entries[-1].append(SequenceMapper.encode_sequence(line).__str__())
                        remaining_lines -= 1

                    case _:
                        # something went horribly wrong
                        raise IOError("Malformatted FastQ File")

    def decompress_file(self, file):
        with open(file, "r") as file:
            remaining_lines = 0
            result = ""
            for line in file:
                match remaining_lines:
                    case 0:
                        result += line # Sequence Identifier
                        remaining_lines += 1
                    case 1:
                        result += SequenceMapper.decode_sequence(line).__str__() # Raw Sequence
                        remaining_lines += 1
                    case 2:
                        result += line # Descriptor Sequence
                        remaining_lines += 1
                    case 3:
                        result += SequenceMapper.decode_sequence(line).__str__() # Quality Sequence
                        remaining_lines = 0
                    case _:
                        # something went horribly wrong
                        raise IOError("Malformatted FastQ File")
        return result



def main():
    # Test
    file = "test/data/HI.4019.002.index_7.ANN0831_R1.fastq"
    compress(file, "test/data/HI.4019.002.index_7.ANN0831_R1.fastq.compressed")
    # Decompress
    #file = "test/data/HI.4019.002.index_7.ANN0831_R1.fastq.compressed"
    #decompress(file, "test/data/temp.fastq")
    # Todo: Replace encoded newline character with smthg else

if __name__ == "__main__":
    main()