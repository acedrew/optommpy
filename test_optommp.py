import unittest
import optommp


class TestOptommp(unittest.TestCase):

    def test_request_header(self):
        self.assertEqual(optommp.request_header(5, 16).hex(), '00004050')

    def test_pack_block_read_request(self):
        self.assertEqual(optommp.pack_block_read_request(
            int('0xfffff0400100', 16), 32, 16).hex(),
            '000040500000fffff040010000200000')

    def test_unpack_block_read_response(self):
        self.assertEqual(
            optommp.unpack_block_read_response(bytes.fromhex(
                '0000407000000000000000000020000000000000000000000007a7c300000'
                '00000000000000000000000000000000000')),
            (0, 0, 501699, 0, 0, 0, 0, 0))

    def test_pack_quadlet_read_requests(self):
        self.assertEqual(
            optommp.pack_quadlet_read_request(int('0xfffff0400108', 16)).hex(),
            '000040400000fffff0400108')

    def test_unpack_quadlet_read_response(self):
        self.assertEqual(optommp.unpack_quadlet_read_response(
            bytes.fromhex('0000406000000000000000000007a7c3')), 501699)


if __name__ == "__main__":
    unittest.main()
