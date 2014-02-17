import gmpy2
from gmpy2 import mpz, powmod, divm


p \
    = \
    mpz(
        '13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171');

g \
    = \
    mpz(
        '11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568');

h \
    = \
    mpz(
        '3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333');

B = mpz(2 ** 20)


def discreteLog(p, g, h):
    intermidiateXs = getIntermidiateX(p, g, h)

    x0 = intermidiateXs[0]
    x1 = intermidiateXs[1]

    return x0 * B + x1

def getIntermidiateX(p, g, h):
    table = {}

    for x1 in range(0, 2 ** 20 + 1):
        denominator = powmod(g, x1, p)
        division = divm(h, denominator, p)
        table[division] = x1
        # print division

    for x0 in range(0, 2 ** 20 + 1):
        rightHandSide = mpz(powmod(powmod(g, B, p), mpz(x0), p))
        # print rightHandSide
        if rightHandSide in table:
            print "Win x0={0}, x1={1}".format(x0, table[rightHandSide])
            return x0, table[rightHandSide]


if __name__ == '__main__':
    print "Discrete log result={0}".format(discreteLog(p, g, h))




