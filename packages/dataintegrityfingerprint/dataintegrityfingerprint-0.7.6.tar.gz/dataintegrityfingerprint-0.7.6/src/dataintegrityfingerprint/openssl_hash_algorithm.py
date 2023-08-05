"""OpenSSL hash algorithms.

This module provides a wrapper for OpenSSL hash functions to have a unique
interface for all types of algorithms.

Each hash algorithm object has the methods `update` and the properties
`checksum` & `hash_algorithm`

"""


import hashlib


class OpenSSLHashAlgorithm(object):
    """OpenSSL hash algorithm."""

    # Currently supported algorithms
    SUPPORTED_ALGORITHMS = sorted(["MD5",
                                   "SHA-1",
                                   "SHA-224",
                                   "SHA-256",
                                   "SHA-384",
                                   "SHA-512",
                                   "SHA3-224",
                                   "SHA3-256",
                                   "SHA3-384",
                                   "SHA3-512"])


    def __init__(self, hash_algorithm):
        """Initialize a OpenSSLHashAlgorithm.

        DIF algorithm naming convention and hashlib algorithm names are
        supported.

        Parameters
        ----------
        hash_algorithm : str
            one of `OpenSSLHashAlgorithm.SUPPORTED_ALGORITHMS`

        """

        self.hash_algorithm = hash_algorithm.upper().replace("_", "-")
        hashlib_name = self.hash_algorithm

        # DIF names deviate from python's hashlib names
        deviating_names = [("MD5", "md5"),
                           ("SHA-1", "sha1"),
                           ("SHA-224", "sha224"),
                           ("SHA-256", "sha256"),
                           ("SHA-384", "sha384"),
                           ("SHA-512", "sha512"),
                           ("SHA3-224", "sha3_224"),
                           ("SHA3-256", "sha3_256"),
                           ("SHA3-384", "sha3_384"),
                           ("SHA3-512", "sha3_512")]
        for dif_name, lib_name in deviating_names:
            if self.hash_algorithm == dif_name or\
                    self.hash_algorithm == lib_name.upper():
                self.hash_algorithm = dif_name
                hashlib_name = lib_name
                break

        if self.hash_algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError("{0} is not a supported hash algorithm.".format(
                self.hash_algorithm))

        self._hasher = hashlib.new(hashlib_name)


    def update(self, data):
        """Update the hash.

        Parameters
        ----------
        data : bytes
            the data to update the hash with

        """

        self._hasher.update(data)

    @property
    def checksum(self):
        return self._hasher.hexdigest()

    @property
    def digest_size(self):
        return self._hasher.digest_size
