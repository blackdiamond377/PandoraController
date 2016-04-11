# A package for naming opcodes used for server communication
# One-byte opcodes are followed by variable data lengths
# Server knows how much data to receive based on opcode

PLAY           = b'\x00'
PAUSE          = b'\x01'
NEXT           = b'\x02'
SELECT_STATION = b'\x03'
GET_SONG       = b'\x04'

QUIT           = b'\x10'

ACK            = b'\xFF'

