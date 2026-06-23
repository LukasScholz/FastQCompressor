import FastQCompressor.struct.SequenceMapper as SequenceMapper

class FastQ:
    def __init__(self):
        self.entries = []

    def read(self, file):
        with open(file, "r") as file:
            lineskip = 0
            for line in file:
                # Sequence identifier
                if line.startswith("@"):
                    lineskip = 4

                match lineskip:

                    case 0:
                        # do not store info outside FastQ sequences
                        continue

                    case 4:
                        # line is identifier -> append new entry
                        self.entries.append([line])
                        lineskip -= 1

                    case 3:
                        # line is raw sequence
                        self.entries[-1].append(SequenceMapper.encode_sequence(line))
                        lineskip -= 1

                    case 2:
                        # line is descriptor sequence
                        self.entries[-1].append(line)
                        lineskip -= 1

                    case 1:
                        # line is quality sequence
                        self.entries[-1].append(SequenceMapper.encode_sequence(line))
                        lineskip -= 1

                    case _:
                        # something went horribly wrong
                        raise IOError("Malformatted FastQ File")


def main():
    file = "test/data/HI.4019.002.index_7.ANN0831_R1.fastq"
    fastq = FastQ()
    fastq.read(file)
    print(fastq.entries)
    with open("test/data/HI.4019.002.index_7.ANN0831_R1.fastq.compressed", "w") as file:
        file.write(str(fastq.entries))


if __name__ == "__main__":
    main()