# checksum_kit_py

Streaming CRC-32 and Adler-32 checksums for Python, with no third-party dependencies.

```python
import io
from checksum_kit_py import crc32_stream, adler32_stream

# Works with any file-like object: open files, BytesIO, sockets wrapped in a buffer.
buf = io.BytesIO(b"hello world")
print(crc32_stream(buf))   # 222957957
print(adler32_stream(buf)) # 436929629
```

## Why this exists

The standard library's `zlib.crc32` and `zlib.adler32` already compute checksums, but they operate on a single `bytes` object.  For large files, reading the whole thing into memory is wasteful or impossible.  This package wires those primitives into a streaming loop so you can checksum a 10 GB file with a few kilobytes of RAM.

The trade-off is simplicity: the functions accept a file-like object and a chunk size, and return the checksum.  They do not buffer, seek, or manage file handles.  If you need incremental checksums across separate calls, call `zlib.crc32` directly with the previous value.

## Edge case

Both functions start with a non-zero initial value (CRC-32 starts at 0, Adler-32 starts at 1).  For an empty stream, `crc32_stream` returns 0 and `adler32_stream` returns 1.  That matches the zlib module's behaviour.

## API

- `crc32_stream(fileobj, chunk_size=65536) -> int`
- `adler32_stream(fileobj, chunk_size=65536) -> int`

Both raise `ValueError` if `chunk_size` is not a positive integer.
