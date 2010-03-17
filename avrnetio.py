import re
import socket

class InsaneExpressionException(Exception): pass
class ErrorRepliedException(Exception): pass

class Sanitizer(object):
    def __init__(self):
        self.saner = {}

    def isSane(self, what, regexp):
        if regexp in self.saner:
            regexp = self.saner[regexp]
        else:
            regexp = re.compile(regexp)
            self.saner[regexp] = regexp
        if ("\r" in what) or ("\n" in what):
            raise InsaneExpressionException("contains newlines")
        if not regexp.match(what):
            raise InsaneExpressionException("re does not match")
sane = Sanitizer().isSane

class AVRNetIO(object):
    def __init__(self, address):
        self.lcdinitialized = False
        self.address = address
        self.ensureConnected()

    def ensureConnected(self):
        self.lcdinitialized = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.address)
        self.sockfile = self.s.makefile('r')

    def getPort(self, portnumber):
        self.s.sendall("GETPORT %d\r\n" % portnumber)
        return self.expect("^[01]$", int)

    def getADC(self, portnumber):
        self.s.sendall("GETADC %d\r\n" % portnumber)
        return self.expect("^[0-9]{1,4}$", int)

    def setPort(self, portnumber, value):
        self.s.sendall("SETPORT %d.%s\r\n" % (portnumber, \
                "1" if value else "0"))
        self.expect("^ACK$")

    def ensureLCDInitialized(self):
        if self.lcdinitialized:
            return
        self.s.sendall("INITLCD\r\n")
        self.expect("^ACK$")
        self.lcdinitialized = True

    def clearLCD(self, line):
        self.ensureLCDInitialized()
        sane(str(line), "^[12]$")
        self.s.sendall("CLEARLCD %d\r\n" % line)
        self.expect("^ACK$")

    def writeLCD(self, line, text):
        self.ensureLCDInitialized()
        sane(str(line), "^[12]$")
        sane(text, r"^[^\.]+$")
        self.s.sendall("WRITELCD %d.%s" % (line, text))
        self.expect("^ACK$")

    def expect(self, regexp, typ=lambda __unused__: None):
        response = self.sockfile.readline()[:-2]
        try:
            sane(response, regexp)
        except InsaneExpressionException:
            raise ErrorRepliedException(response)
        return typ(response)

