#!/usr/bin/python


# In this project you will implement two encryption/decryption systems, one using AES in CBC mode and another using AES
# in counter mode (CTR). In both cases the 16-byte encryption IV is chosen at random and is prepended to the ciphertext.
# For CBC encryption we use the PKCS5 padding scheme discussed in class (13:50).
#
# While we ask that you implement both encryption and decryption, we will only test the decryption function.
# In the following questions you are given an AES key and a ciphertext (both are hex encoded) and your goal is to recover
# the plaintext and enter it in the input boxes provided below.
#
# For an implementation of AES you may use an existing crypto library such as PyCrypto (Python), Crypto++ (C++), or any other.
# While it is fine to use the built-in AES functions, we ask that as a learning experience you implement CBC and CTR modes yourself.
#
#
# Question 1

# CBC key: 140b41b22a29beb4061bda66b6747e14
# CBC Ciphertext 1:
# 4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee \
#     2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81

# Question 1
# CBC key: 140b41b22a29beb4061bda66b6747e14
# CBC Ciphertext 1:
# 4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee \
#     2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81
# Answer for Question 1
#
# Question 2
# CBC key: 140b41b22a29beb4061bda66b6747e14
# CBC Ciphertext 2:
# 5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48 \
#     e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253
# Answer for Question 2
#
# Question 3
# CTR key: 36f18357be4dbd77f050515c73fcf9f2
# CTR Ciphertext 1:
# 69dda8455c7dd4254bf353b773304eec
# 0ec7702330098ce7f7520d1cbbb20fc3
# 88d1b0adb5054dbd7370849dbf0b88d3
# 93f252e764f1f5f7ad97ef79d59ce29f
# 5f51eeca32eabedd9afa9329
# Answer for Question 3
#
# Question 4
# CTR key: 36f18357be4dbd77f050515c73fcf9f2
# CTR Ciphertext 2:
# 770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa \
#     0e311bde9d4e01726d3184c34451
# Answer for Question 4


from Crypto.Cipher import AES

HEXENC_BLOCKSIZE = 32

problemSetCBC = [
    {"key": "140b41b22a29beb4061bda66b6747e14",
     "ct": "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"}
    , {"key": "140b41b22a29beb4061bda66b6747e14",
       "ct": "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"}]

problemSetCTR = [
    {"key": "36f18357be4dbd77f050515c73fcf9f2",
     "ct": "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"}
    , {"key": "36f18357be4dbd77f050515c73fcf9f2",
       "ct": "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"}]


def autoDecryptCBC(key, cipherText):
    iv = cipherText[0:32].decode('hex')
    crypto = AES.new(key.decode("hex"), AES.MODE_CBC, iv)
    print crypto.decrypt(cipherText[HEXENC_BLOCKSIZE:].decode("hex"))


def autoDecryptCTR(key, cipherText):
    iv = cipherText[0:32].decode('hex')
    crypto = AES.new(key.decode("hex"), AES.MODE_CTR, iv)
    print crypto.decrypt(cipherText[HEXENC_BLOCKSIZE:].decode("hex"))


def aesECBDecrypt(key, cipherBlock):
    crypto = AES.new(key.decode("hex"), AES.MODE_ECB)
    return crypto.decrypt(cipherBlock.decode("hex")).encode("hex")

def aesECBEncrypt(key, cipherBlock):
    crypto = AES.new(key.decode("hex"), AES.MODE_ECB)
    return crypto.encrypt(cipherBlock.decode("hex")).encode("hex")


def hexxor(a, b):
    from Crypto.Util.strxor import strxor

    return strxor(a.decode('hex'), b.decode('hex')).encode('hex')


def decryptCBC(key, cipherText):
    result = ""
    iv = cipherText[0:HEXENC_BLOCKSIZE]
    cipherText = cipherText[HEXENC_BLOCKSIZE:]
    x = 0

    if len(cipherText) % 2 != 0:
        print "WARN: Padding is needed"

    while x < len(cipherText):
        cipherBlock = cipherText[x:x + HEXENC_BLOCKSIZE]
        blockCBCresult = aesECBDecrypt(key, cipherBlock)

        if x == 0:
            result += hexxor(blockCBCresult, iv)
        else:
            result += hexxor(blockCBCresult, cipherText[x - HEXENC_BLOCKSIZE:x])

        x += HEXENC_BLOCKSIZE

    return result.decode('hex')


def hexAdd(hexString, number):

    intValue = int(hexString, 16) + 1
    hexValue = hex(intValue)[2:-1]
    if len(hexValue) % 2 != 0:
        return '0' + hexValue

    return hexValue

def decryptCTR(key, cipherText):
    result = ""
    iv = cipherText[0:HEXENC_BLOCKSIZE]
    cipherText = cipherText[HEXENC_BLOCKSIZE:]
    x = 0

    while x < len(cipherText):
        cipherBlock = cipherText[x:x + HEXENC_BLOCKSIZE]

        if len(cipherBlock) < 32:
            cipherBlock += "0" * (32 - len(cipherBlock))

        aesBlock = aesECBEncrypt(key, iv)

        result += hexxor(aesBlock, cipherBlock)

        iv = hexAdd(iv, 1)
        x += HEXENC_BLOCKSIZE

    return result.decode('hex')


if __name__ == '__main__':
    for problem in problemSetCBC:
        print "CBC:" + decryptCBC(problem["key"], problem["ct"])


    for problem in problemSetCTR:
        print "CTR:" + decryptCTR(problem["key"], problem["ct"])


