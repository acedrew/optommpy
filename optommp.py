import struct


def request_header(tl, tcode):
    # universal request header, 4 Bytes long
    return struct.pack('>2xBB', (tl << 2), (tcode << 4))


def pack_quadlet_read_request(start_address, tl=16):
    return struct.pack('>4s2xHI', request_header(tl, 4),
                       (start_address >> 32), (start_address & (2 ** 32 - 1)))


def pack_block_read_request(start_address, data_length, tl=16):
    # This packs the arguments into the message format specified
    # by Opto22 Form 1465 "OptoMMP Protocol Guide"
    return struct.pack('>4s2xHIH2x', request_header(tl, 5),
                       (start_address >> 32), (start_address & (2 ** 32 - 1)),
                       data_length)


def verify_response_header(response, tcode, tl=16):
    # First we unpack the the header data, and verify there were no errors and
    # the TL code is correct.
    r_tl, r_tcode, r_rcode = struct.unpack('>2x2B2xBx', response[:8])
    if(r_tl >> 2 != tl) or (r_tcode >> 4 != tcode) or (r_rcode != 0):
        raise IOError
    else:
        return response[8:]


def unpack_quadlet_read_response(response, tl=16):
    verified = verify_response_header(response, 7, tl)
    return struct.unpack('>4xI', verified)


def unpack_block_read_response(response, tl=16):
    verified = verify_response_header(response, 7, tl)
    length, = struct.unpack('>4xH2x', verified[:8])
    # now we unpack the rest of the data, this assumes 32bit uints. This
    # returns a tuple of the values
    numbers = length // 4
    return struct.unpack('>' + str(numbers) + 'I', verified[8:])
