""" Zlib hash algorithms.

This module provides a wrapper for zlib hash functions to have a unique
interface for all types of algorithms.

Each hash algorithm object has the methods `update` and the properties
`checksum` & `hash_algorithm`

"""

import zlib


class ZlibHashAlgorithm(object):
    """Zlib hash algorithm."""

    SUPPORTED_ALGORITHMS = sorted(["CRC-32",
                                   "ADLER-32"])

    def __init__(self, hash_algorithm):
        """Initialize a ZlibHashAlgorithm.

        DIF algorithm naming convention and hashlib algorithm names are
        supported.

        Parameters
        ----------
        hash_algorithm : str
            one of `ZlibHashAlgorithm.SUPPORTED_ALGORITHMS`

        """

        hash_algorithm = hash_algorithm.upper().replace("_", "-")
        if hash_algorithm == "CRC-32":
            self._current = 0
            self._hasher = zlib.crc32
        elif hash_algorithm == "ADLER-32":
            self._current = None
            self._hasher = zlib.adler32
        else:
            raise ValueError("{0} is not a supported hash algorithm.".format(
                hash_algorithm))
        self.hash_algorithm = hash_algorithm

    def update(self, data):
        """Update the hash.

        Parameters
        ----------
        data : bytes
            the data to update the hash with

        """

        try:
            self._current = self._hasher(data, self._current)
        except:
            self._current = self._hasher(data)

    @property
    def checksum(self):
        return hex(self._current)[2:]
