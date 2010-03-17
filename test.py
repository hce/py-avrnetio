import avrnetio

def doit():
    x = avrnetio.AVRNetIO(('192.168.0.90', 50290))
    x.getPort(1)

if __name__ == '__main__':
    doit()
