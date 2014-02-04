import paddingQuery as pq
import homework2 as util

TARGET_CIPHERTEXT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
BLOCK_SIZE_IN_BYTES = 16


def padAttack(cipherText):
    endPosition = len(cipherText)
    startPosition = BLOCK_SIZE_IN_BYTES * 2
    currentPT = ""
    oracleQuery = pq.PaddingOracle()
    stepCount = 1

    for index in range(endPosition, startPosition, -2):
        stepHex = ord(stepCount).encode('hex')
        cipherByte = cipherText[index - 2:index]
        for trialByte in [chr(x).encode('hex') for x in range(0, 256)]:

            trialByte = util.hexxor(util.hexxor(trialByte,stepHex),cipherByte)
            print ("Using trialByte=%")
            queryString = cipherText[0:index - 2] + trialByte + currentPT
            if len(queryString) != len(cipherText):
                raise Exception("Something went wrong building query")

            queryResult = oracleQuery.query(queryString)

            if queryResult == True:
                print "Match with byte: ", trialByte
                currentPT += trialByte
                stepCount++
                break



if __name__ == '__main__':
    padAttack(TARGET_CIPHERTEXT)