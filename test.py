import avrnetio
import time

def doit():
    x = avrnetio.AVRNetIO(('192.168.0.90', 50290))
    for i in range(1, 5):
        print "Status of port %d: %d" % (i, x.getPort(i))
    for i in range(1, 5):
        print "A/D port %d: %d" % (i, x.getADC(i))
    print "Setting ports:"
    for i in range(0, 16):
        x.setPort((i % 8) + 1, i < 8)
        print "Set port %d to %s." % ((i % 8) + 1, i < 8)
        time.sleep(0.1)

    print "Clearing LCD"
    x.clearLCD(1)
    x.clearLCD(2)
    print "Writing Hello World."
    x.writeLCD(1, "Hello")
    x.writeLCD(2, "World")
    print "Done."

if __name__ == '__main__':
    doit()
