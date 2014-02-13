from __future__ import division
from Crypto.Hash import SHA256
import math
import sys

BLOCK_BYTE_SIZE = 1024

def readFile(filename):
    print "Reading file..."
    file = open(filename, "rb")
    data = file.read()
    file.close()
    print "Byte size: ", len(data)
    print "Block size: ", len(data) / BLOCK_BYTE_SIZE
    return data


def generateHash(bytes):
    blocksToProcess = int(math.ceil(len(bytes) / BLOCK_BYTE_SIZE))
    previousHash = b""

    while blocksToProcess > 0:
        startRange = ((blocksToProcess - 1) * BLOCK_BYTE_SIZE)
        endRange = startRange + BLOCK_BYTE_SIZE
        currentBlock = bytes[startRange:endRange]
        hash = SHA256.new()
        hash.update(currentBlock + previousHash)
        previousHash = hash.digest()
        blocksToProcess -= 1

    print previousHash.encode('hex')

if __name__ == '__main__':
    generateHash(readFile(sys.argv[1]))
