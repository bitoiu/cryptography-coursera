import paddingQuery as pq
import homework2 as util

TARGET_CIPHERTEXT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
BLOCK_SIZE_IN_BYTES = 16


def padAttack(cipherText):
    endPosition = len(cipherText)
    startPosition = BLOCK_SIZE_IN_BYTES * 2
    currentPT = ""
    oracleQuery = pq.PaddingOracle()

    for index in range(endPosition, startPosition, -2):
        step = (endPosition - index) / 2;
        pad = chr(step).encode('hex') * (step + 1)
        cipherSection = cipherText[index - 2:endPosition]

        if len(pad) != len(cipherSection):
            raise Exception("CT suffix and pad should be same length")

        padXorCipher = util.hexxor(pad, cipherSection)

        for trialByte in [chr(x).encode('hex') for x in range(0, 256)]:

            trialSection = trialByte + currentPT

            if len(padXorCipher) != len(trialSection):
                raise Exception("different lengths for trial byte and pad/cipher xor")

            trialPad = util.hexxor(trialSection,padXorCipher)

            queryString = cipherText[0:index - 2] + trialPad
            queryResult = oracleQuery.query(queryString)

            if queryResult == True:
                print "Match with byte: ", trialByte
                currentPT += trialByte
                break

    return currentPT



if __name__ == '__main__':
    print padAttack(TARGET_CIPHERTEXT)