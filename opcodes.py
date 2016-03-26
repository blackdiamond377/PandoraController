# A package for naming opcodes used for server communication
# One-byte opcodes are followed by variable data lengths
# Server knows how much data to recieve based on opcode

PLAY           = b'\x00'
PAUSE          = b'\x01'
NEXT           = b'\x02'
SELECT_STATION = b'\x03'
QUIT           = b'\x04'

ACK            = b'\xFF'

