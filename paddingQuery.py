#!/usr/bin/python

import urllib2
import sys
import random

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):

        #return random.randint(1, 2) == 1
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding


if __name__ == "__main__":
    po = PaddingOracle()
    po.query(sys.argv[1])       # Issue HTTP query with the given argument