import math
import ast

SEPERATOR = chr(182)



class SequencePacker:
    def __init__(self, sequence: bytes, length : int, alphabet : list):
        self.sequence = sequence
        self.length = length
        self.alphabet = alphabet

    def __str__(self) -> str:
        return str(self.length) + SEPERATOR + self.sequence.decode() + SEPERATOR + str(self.alphabet)





def encode_sequence(sequence):
    alphabet = sorted(set(sequence))
    n = len(alphabet)
    bits_per_char = max(1, math.ceil(math.log2(n)))
    encode_map = {c: i for i, c in enumerate(alphabet)}

    bitstream = 0
    total_bits = 0

    for c in sequence:
        bitstream = (bitstream << bits_per_char) | encode_map[c]
        total_bits += bits_per_char

    padding = (8 - total_bits % 8) % 8
    bitstream <<= padding
    total_bits += padding

    encoded = bitstream.to_bytes(total_bits // 8, byteorder="big")

    return SequencePacker(encoded, len(sequence), alphabet)


def _decode_packed_sequence(sequencepacker : SequencePacker):
    n = len(sequencepacker.alphabet)
    bits_per_char = max(1, math.ceil(math.log2(n)))
    bitstream = int.from_bytes(sequencepacker.sequence, byteorder="big")
    total_bits = len(sequencepacker.sequence) * 8
    padding = total_bits - sequencepacker.length * bits_per_char
    bitstream >>= padding
    mask = (1 << bits_per_char) - 1

    chars = []
    for i in range(sequencepacker.length):
        shift = (sequencepacker.length - 1 - i) * bits_per_char
        code = (bitstream >> shift) & mask
        chars.append(sequencepacker.alphabet[code])

    return "".join(chars)


def decode_sequence(sequence : str) -> str:
    datalist = sequence.split(SEPERATOR)
    sequencepacker = SequencePacker(datalist[1].encode(), int(datalist[0]), ast.literal_eval(datalist[2]))
    return _decode_packed_sequence(sequencepacker)

def main():
    ## Test
    text = "ABCDABCDABCD"

    sequencepacker = encode_sequence(text)
    print(sequencepacker.__str__())

    print(sequencepacker.sequence)
    print(len(sequencepacker.sequence))
    print(sequencepacker.alphabet)

    decoded = decode_sequence(sequencepacker.__str__())
    print(decoded)
    print(len(decoded))
    print()

if __name__ == "__main__":
    main()