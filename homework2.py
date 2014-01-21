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

from Crypto.Cipher import AES


def decryptCBC(key, cipherText):
    iv = cipherText[0:32].decode('hex')

    crypto = AES.new(key.decode("hex"), AES.MODE_CBC, iv)
    print crypto.decrypt(cipherText[32:].decode("hex"))


if __name__ == '__main__':
    key = "140b41b22a29beb4061bda66b6747e14"
    cipherText = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

    decryptCBC(key, cipherText)
