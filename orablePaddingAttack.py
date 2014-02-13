import paddingQuery as pq
import cbcdecryption as util

TARGET_CIPHERTEXT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
BLOCK_SIZE_IN_BYTES = 16
BLOCK_SIZE_HEXENC = BLOCK_SIZE_IN_BYTES * 2


def getCipherAdjustment(targetPad, intermediateBlock):
    result = ""
    for x in range(0, len(intermediateBlock), 2):
        result += util.hexxor(targetPad, intermediateBlock[x:x + 2])
    return result


def padAttack(cipherText):
    ctLength = len(cipherText)
    ctBlockLength = ctLength / BLOCK_SIZE_HEXENC
    plaintText = ""

    for blockIndex in range(0, ctBlockLength - 1):

        startPosition = blockIndex * BLOCK_SIZE_HEXENC
        endPosition = startPosition + BLOCK_SIZE_HEXENC
        oracleQuery = pq.PaddingOracle()
        intermediateBlock = ""
        blockPlainText = ""
        isLastBlock = blockIndex == ctBlockLength - 2
        winnerByte = ""

        for index in range(endPosition, startPosition, -2):
            step = (endPosition - index) / 2 + 1
            stepHex = chr(step).encode('hex')
            originalCipherByte = cipherText[index - 2:index]

            cipherAdjustment = getCipherAdjustment(stepHex, intermediateBlock)

            for trialByte in [chr(x).encode('hex') for x in range(0, 256)]:

                winnerByte = None
                firstPart = cipherText[0:index - 2]
                lastPart = cipherText[endPosition:endPosition + 32]
                queryString = firstPart + trialByte + cipherAdjustment + lastPart
                #print "{0} - {1} - {2} - {3}".format(firstPart, trialByte, cipherAdjustment, lastPart)

                if len(queryString) % 32 != 0:
                    raise Exception("Submitting a query which is not a multiple of 32 HexEncoded")

                queryResult = oracleQuery.query(queryString)

                if queryResult:
                    winnerByte = trialByte
                    break

                # will not work for ct with exactly one byte pad
                if isLastBlock and queryResult is None and step > 1:
                    print "special 200 scenario"
                    winnerByte = trialByte
                    break

            if winnerByte is None:
                raise Exception("No match found in last step")

            intermediateByte = util.hexxor(winnerByte, stepHex)
            intermediateBlock = intermediateByte + intermediateBlock;
            plainTextByte = util.hexxor(originalCipherByte, intermediateByte)
            blockPlainText = plainTextByte + blockPlainText

            print "Original ct byte={0}".format(originalCipherByte)
            print "Match with guess={0}".format(winnerByte)
            print "Intermediate byte={0}".format(intermediateByte)
            print "Plaint text byte={0}".format(plainTextByte)
            print "Plain text block so far={0}", format(blockPlainText)

        plaintText += blockPlainText

    return plaintText


if __name__ == '__main__':
    print padAttack(TARGET_CIPHERTEXT)
