import struct

# http://www.bortzmeyer.org/4934.html
def format_32():
    # Get the size of C integers. We need 32 bits unsigned.
    format_32 = ">I"
    if struct.calcsize(format_32) < 4:
        format_32 = ">L"
        if struct.calcsize(format_32) != 4:
            raise Exception("Cannot find a 32 bits integer")
    elif struct.calcsize(format_32) > 4:
        format_32 = ">H"
        if struct.calcsize(format_32) != 4:
            raise Exception("Cannot find a 32 bits integer")
    else:
        pass
    return format_32

FORMAT_32 = format_32()

def int_from_net(data):
    return struct.unpack(FORMAT_32, data)[0]

def int_to_net(value):
    return struct.pack(FORMAT_32, value)

def write(socket, data):
    # +4 for the length field itself (section 4 mandates that)
    # +2 for the CRLF at the end
    length = int_to_net(len(data) + 4 + 2)
    socket.settimeout(20)
    socket.send(length)
    sended = socket.send(data + "\r\n")
    socket.settimeout(None)
    return sended

def read(socket):
    socket.settimeout(20)
    net = socket.recv(4)
    if net:
        length = int_from_net(net)-4
        buffer = ''
        while (length>len(buffer)):
            buffer += socket.recv(4096)
        socket.settimeout(None)
        return buffer
    else:
        socket.settimeout(None)

