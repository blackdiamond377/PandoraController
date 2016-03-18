# A package for naming opcodes used for server communication
# One-byte opcodes are followed by variable data lengths
# Server knows how much data to recieve based on opcode

PLAY           = 0x00
PAUSE          = 0x01
SELECT_STATION = 0x02
QUIT           = 0X03

