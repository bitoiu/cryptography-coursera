import paddingQuery as pq
import homework2 as util

TARGET_CIPHERTEXT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
BLOCK_SIZE_IN_BYTES = 16
BLOCK_SIZE_HEXENC = BLOCK_SIZE_IN_BYTES * 2


def getCipherAdjustment(targetPad, intermediateBlock):

    result = ""
    for x in range(0, len(intermediateBlock),2):
        result += util.hexxor(targetPad, intermediateBlock[x:x+2])
    return result


def padAttack(cipherText):
    ctLength = len(cipherText)
    ctBlockLength = ctLength / BLOCK_SIZE_HEXENC
    plaintText = ""

    for blockIndex in range(0, ctBlockLength - 1):

        if blockIndex < 2: continue

        startPosition = blockIndex * BLOCK_SIZE_HEXENC
        endPosition = startPosition + BLOCK_SIZE_HEXENC
        oracleQuery = pq.PaddingOracle()
        intermediateBlock = ""
        blockPlainText = ""

        for index in range(endPosition, startPosition, -2):
            step = (endPosition - index) / 2 + 1
            stepHex = chr(step).encode('hex')
            pad = stepHex * step
            originalCipherByte = cipherText[index - 2:index]

            cipherAdjustment = getCipherAdjustment(stepHex, intermediateBlock)

            for trialByte in [chr(x).encode('hex') for x in range(0, 256)]:


                firstPart = cipherText[0:index - 2]
                lastPart = cipherText[endPosition:endPosition + 32]
                queryString = firstPart + trialByte + cipherAdjustment + lastPart
                print "{0} - {1} - {2} - {3}".format(firstPart, trialByte, cipherAdjustment, lastPart)

                if len(queryString) % 32 != 0:
                    raise Exception("Submitting a query which is not a multiple of 32 HexEncoded")

                queryResult = oracleQuery.query(queryString)

                if queryResult:
                    intermediateByte = util.hexxor(trialByte, stepHex)
                    intermediateBlock = intermediateByte + intermediateBlock;
                    plainTextByte = util.hexxor(originalCipherByte, intermediateByte)
                    blockPlainText = plainTextByte + blockPlainText

                    print "Match with guess={0}".format(trialByte)
                    print "Intermediate byte={0}".format(intermediateByte)
                    print "Plaint text byte={0}".format(plainTextByte)
                    break

            if len(intermediateBlock) != len(pad):
                raise Exception("No success finding a match for query")

        plaintText = blockPlainText + plaintText

    return plaintText


if __name__ == '__main__':
    print padAttack(TARGET_CIPHERTEXT)
