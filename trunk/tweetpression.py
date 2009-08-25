#
# To run tests:
# $ python tweetpression.py
#

from compulsion import Url

LITTLE = True
BIG = False

class BasedNumber(object):
    """Represents a number and provides functions for handling numbers as lists of digits in arbitrary bases."""

    def __init__(self, decimal=None, digits=None, base=10, endianness=LITTLE):
        self.value = 0

        if decimal and digits:
            raise Exception("A BasedNumber cannot be initialised with both a decimal and a list of digits.")
        
        if decimal:
            self.value = decimal

        elif digits:
            if endianness is BIG:
                digits.reverse()
            for i in xrange(0, len(digits)):
                self.value += digits[i] * (base**i)
        
    def radix(self, base):
        """Returns a little-endian list of decimal numbers representing the number in the given base."""
        if base < 2:
            raise Exception("base argument must be greater than 1.")
        
        digits = []
        carry = self.value
        while carry > 0:
            quotient = carry / base
            remainder = carry % base
            digits.append(remainder)
            carry = quotient
        return digits
        
    @classmethod
    def from_7bit_string(cls, string):
        """Converts a non-extended ASCII string to a BasedNumber object. The first character is taken as the least significant digit."""
        digits = []
        for char in string:
            val = ord(char)
            if val > 127:
                raise Exception("The string contains extended characters.")
            digits.append(val)
        return BasedNumber(digits=digits, base=128)
        
    def __repr__(self):
        return "<BasedNumber %s>" % self.value

### TESTING

print "Tweetpression.py (c) Alex Macmillan, Joe Lanman 2009"
print

def test_url(testurl):
    url = Url(testurl)
    print "URL:                         ", url
    print "URL length (chars):          ", len(url)
    print "URL length (bits):           ", len(url) * 8
    fivebitseq = url.to_5bit()
    print "5-bit encoded length (chars):", len(fivebitseq)
    print "5-bit encoded length (bits): ", len(fivebitseq) * 5
    print "Bit compression ratio:       ", "%.02f%%" % ((len(fivebitseq) * 5.0) / (len(url) * 8) * 100)
    urlnum = BasedNumber(digits=fivebitseq, base=2**5)
    print "URL, 5-bit, decimal:         ", urlnum
    b20000seq = urlnum.radix(20000)
    print "URL, 5-bit, base 20000:      ", b20000seq
    print "Char compression ratio:      ", "%.02f%%" % ((len(b20000seq) * 1.0) / (len(url)) * 100)
    print

onethousand = BasedNumber(1000)
print "1000:                        ", onethousand
print "1000, base 10:               ", onethousand.radix(10)
print "1000, base 2:                ", onethousand.radix(2)
print

fivetwelve = BasedNumber(512)
print "512:                         ", fivetwelve
print "512, base 2:                 ", fivetwelve.radix(2)
print "512, base 16:                ", fivetwelve.radix(16)
print

helloworld = BasedNumber.from_7bit_string("Hello, world!")
print "Hello, world!                ", helloworld
print "Hello, world!, base 128:     ", helloworld.radix(128)
print "Hello, world!, base 20000:   ", helloworld.radix(20000)
print

print "A short URL with very low entropy."
test_url("http://www.slashdot.org/")

print "A long URL primarily using lower case characters."
test_url("http://www.lyricsmode.com/lyrics/f/florence_and_the_machine/a_kiss_with_a_fist_is_better_than_none.html")

print "An Amazon URL with mixed case, special chars."
test_url("http://www.amazon.co.uk/Pragmatic-Programmer-Andrew-Hunt/dp/020161622X/ref=sr_1_1?ie=UTF8&s=books&qid=1247419421&sr=8-1")