import io
import unittest
import zlib

from checksum_kit_py import crc32_stream, adler32_stream


class TestCrc32Stream(unittest.TestCase):
    def test_empty_stream(self):
        self.assertEqual(crc32_stream(io.BytesIO(b"")), 0)

    def test_known_values(self):
        data = b"123456789"
        self.assertEqual(crc32_stream(io.BytesIO(data)), zlib.crc32(data))

    def test_chunk_boundaries(self):
        data = b"abcdefghij"
        expected = zlib.crc32(data)
        for chunk_size in (1, 2, 3, 4, 5, 10):
            with self.subTest(chunk_size=chunk_size):
                self.assertEqual(crc32_stream(io.BytesIO(data), chunk_size), expected)

    def test_large_data(self):
        data = bytes(range(256)) * 1000
        self.assertEqual(crc32_stream(io.BytesIO(data)), zlib.crc32(data))

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            crc32_stream(io.BytesIO(b""), 0)
        with self.assertRaises(ValueError):
            crc32_stream(io.BytesIO(b""), -1)
        with self.assertRaises(ValueError):
            crc32_stream(io.BytesIO(b""), 1.5)


class TestAdler32Stream(unittest.TestCase):
    def test_empty_stream(self):
        self.assertEqual(adler32_stream(io.BytesIO(b"")), 1)

    def test_known_values(self):
        data = b"123456789"
        self.assertEqual(adler32_stream(io.BytesIO(data)), zlib.adler32(data))

    def test_chunk_boundaries(self):
        data = b"abcdefghij"
        expected = zlib.adler32(data)
        for chunk_size in (1, 2, 3, 4, 5, 10):
            with self.subTest(chunk_size=chunk_size):
                self.assertEqual(adler32_stream(io.BytesIO(data), chunk_size), expected)

    def test_large_data(self):
        data = bytes(range(256)) * 1000
        self.assertEqual(adler32_stream(io.BytesIO(data)), zlib.adler32(data))

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            adler32_stream(io.BytesIO(b""), 0)
        with self.assertRaises(ValueError):
            adler32_stream(io.BytesIO(b""), -1)
        with self.assertRaises(ValueError):
            adler32_stream(io.BytesIO(b""), 1.5)


if __name__ == "__main__":
    unittest.main()
