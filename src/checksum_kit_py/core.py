"""Core checksum algorithms that operate on streams.

Both functions read from a file-like object in chunks and never load the
entire input into memory.  The chunk size is a parameter so callers can
tune the memory/throughput trade-off for their environment.
"""

import zlib


def crc32_stream(fileobj, chunk_size=65536):
    """Compute the CRC-32 checksum of a binary stream.

    Parameters
    ----------
    fileobj : file-like
        Any object with a ``read(size)`` method that returns bytes.
    chunk_size : int, optional
        Number of bytes to read per iteration.  Must be positive.

    Returns
    -------
    int
        The CRC-32 checksum as an unsigned 32-bit integer.

    Raises
    ------
    ValueError
        If *chunk_size* is not a positive integer.
    """
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    checksum = 0
    while True:
        chunk = fileobj.read(chunk_size)
        if not chunk:
            break
        checksum = zlib.crc32(chunk, checksum)
    return checksum & 0xFFFFFFFF


def adler32_stream(fileobj, chunk_size=65536):
    """Compute the Adler-32 checksum of a binary stream.

    Parameters
    ----------
    fileobj : file-like
        Any object with a ``read(size)`` method that returns bytes.
    chunk_size : int, optional
        Number of bytes to read per iteration.  Must be positive.

    Returns
    -------
    int
        The Adler-32 checksum as an unsigned 32-bit integer.

    Raises
    ------
    ValueError
        If *chunk_size* is not a positive integer.
    """
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    checksum = 1
    while True:
        chunk = fileobj.read(chunk_size)
        if not chunk:
            break
        checksum = zlib.adler32(chunk, checksum)
    return checksum & 0xFFFFFFFF
