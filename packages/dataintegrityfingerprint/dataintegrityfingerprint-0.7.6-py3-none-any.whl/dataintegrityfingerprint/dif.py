"""Data Intergrity Fingerprint (DIF) programming library.

Import as `dataintegrityfingerprint`.

"""


import os
import codecs
import multiprocessing

from .openssl_hash_algorithm import OpenSSLHashAlgorithm
from .zlib_hash_algorithm import ZlibHashAlgorithm


class DataIntegrityFingerprint:
    """A class representing a DataIntegrityFingerprint (DIF).

    Example
    -------
    dif = DataIntegrityFingerprint("~/Downloads")
    print(dif)
    print(dif.checksums)

    """

    CRYPTOGRAPHIC_ALGORITHMS = OpenSSLHashAlgorithm.SUPPORTED_ALGORITHMS
    NON_CRYPTOGRAPHIC_ALGORITHMS = ZlibHashAlgorithm.SUPPORTED_ALGORITHMS
    CHECKSUM_FILENAME_SEPARATOR = "  "

    def __init__(self, data, from_checksums_file=False,
                 hash_algorithm="SHA-256", multiprocessing=True,
                 allow_non_cryptographic_algorithms=False):
        """Create a DataIntegrityFingerprint object.

        Parameters
        ----------
        data : str
            the path to the data
        from_checksums_file : bool
            data argument is a checksums file
        hash_algorithm : str
            the hash algorithm (optional, default: sha256)
        multiprocessing : bool
            using multi CPU cores (optional, default: True)
            speeds up creating of checksums for large data files
        allow_non_cryptographic_algorithms : bool
            set True only, if you need non cryptographic algorithms (see
            notes!)

        Note
        ----
        We do not suggest to use non-cryptographic algorithms.
        Non-cryptographic algorithms are, while much faster, not secure (e.g.
        can be tempered with). Only use these algorithms to check for technical
        file damage and in cases security is not of critical concern.

        """

        if not from_checksums_file:
            assert os.path.isdir(data)

        h = new_hash_instance(hash_algorithm,
                              allow_non_cryptographic_algorithms)
        self._hash_algorithm = h.hash_algorithm
        self._data = os.path.abspath(data)
        self._file_count = None
        self._hash_list = []
        self._multiprocessing = multiprocessing
        self._allow_non_cryptographic_algorithms = \
            allow_non_cryptographic_algorithms

    def __str__(self):
        return str(self.dif)

    def get_files(self):
        """Get all files to hash.

        Returns
        -------
        files : list
            the list of files to hash

        """

        rtn = []
        if os.path.isdir(self._data):
            for dir_, _, files in os.walk(self._data, followlinks=True):
                for filename in files:
                    rtn.append(os.path.join(dir_, filename))
        self._file_count = len(rtn)
        return rtn

    @ property
    def hash_algorithm(self):
        return self._hash_algorithm

    @property
    def data(self):
        return self._data

    @property
    def file_hash_list(self):
        if len(self._hash_list) < 1:
            self.generate()
        return self._hash_list

    @property
    def checksums(self):
        rtn = ""
        for h, fl in sorted(self.file_hash_list, key=lambda x: x[1]):
            rtn += u"{0}{1}{2}\n".format(h, self.CHECKSUM_FILENAME_SEPARATOR,
                                         fl)
        return rtn

    @property
    def dif(self):
        if len(self.file_hash_list) < 1:
            return None

        hasher = new_hash_instance(self._hash_algorithm,
                                   self.allow_non_cryptographic_algorithms)
        concat = "".join(["".join(x) for x in self.file_hash_list])
        hasher.update(concat.encode("utf-8"))
        return hasher.checksum

    @property
    def file_count(self):
        if self._file_count is None:
            self.get_files()
        return self._file_count

    @property
    def multiprocessing(self):
        return self._multiprocessing

    @property
    def allow_non_cryptographic_algorithms(self):
        return self._allow_non_cryptographic_algorithms

    def generate(self, progress=None):
        """Generate hash list to get Data Integrity Fingerprint.

        Parameters
        ----------
        progress: function, optional
            a callback function for a progress reporting that takes the
            following parameters:
                count  -- the current count
                total  -- the total count
                status -- a string describing the status

        """

        hash_list = []

        if os.path.isfile(self._data):
            # from  checksum file
            with codecs.open(self._data, encoding="utf-8") as f:
                for line in f:
                    h, fl = line.split(self.CHECKSUM_FILENAME_SEPARATOR,
                                       maxsplit=1)
                    hash_list.append((h, fl.strip()))
        else:
            files = self.get_files()
            func_args = zip(files, [self._hash_algorithm] * len(files))
            if self.multiprocessing:
                pool = multiprocessing.Pool()
                imap = pool.imap_unordered
            else:
                imap = map

            for counter, rtn in enumerate(imap(_hash_file_content, func_args)):
                if progress is not None:
                    progress(counter + 1, len(files),
                             "{0}/{1}".format(counter + 1, len(files)))
                fl = os.path.relpath(rtn[1], self.data).replace(os.path.sep,"/")
                hash_list.append((rtn[0], fl))

            if self.multiprocessing:
                pool.close()

        self._hash_list = sorted(hash_list, key=lambda x: x[0] + x[1])

    def save_checksums(self, filename=None):
        """Save the checksums to a file.

        Parameters
        ----------
        filename : str, optional
            the name of the file to save checksums to

        Returns
        -------
        success : bool
            whether saving was successful

        """

        if self.dif is not None:
            if filename is None:
                filename = os.path.split(self.data)[-1] + ".{0}".format(
                    self._hash_algorithm)

            with codecs.open(filename, 'w', "utf-8") as f:
                f.write(self.checksums)

            return True

    def diff_checksums(self, filename):
        """Calculate differences of checksums to checksums file.

        Parameters
        ----------
        filename : str
            the name of the checksums file

        Returns
        -------
        diff : str
            the difference of checksums to the checksums file
            (minus means checksums is missing something from checksums file,
            plus means checksums has something in addition to checksums file)

        """

        checksums = self.checksums.split("\n")
        other = DataIntegrityFingerprint(
            filename, from_checksums_file=True,
            hash_algorithm=self._hash_algorithm,
            allow_non_cryptographic_algorithms=\
                self.allow_non_cryptographic_algorithms)
        checksums_other = other.checksums.split("\n")
        sub = ["- " + x for x in list(set(checksums_other) - set(checksums))]
        add = ["+ " + x for x in list(set(checksums) - set(checksums_other))]

        return "\n".join(["\n".join(sub), "\n".join(add)]).strip()


def new_hash_instance(hash_algorithm,
                      support_non_cryptographic_algorithms=False):
    """Return a new instance of a hash object (similar to hashlib.new()).

    Each HashAlgorithm object has the methods `update` and the
    properties `hash_algorithm` (according the DIF naming convention),
    `checksum`

    Parameters
    ----------
    hash_algorithm : str
        one of `DataIntegrityFingerprint.CRYPTOGRAPHIC_ALGORITHMS`
        (or `DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS`)
    support_non_cryptographic_algorithms : bool
        if True, also allow hash algorithms from
        `DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS`

    Returns
    -------
    hasher : `ZlibHashAlgorithm` or `OpenSSLHashAlgorithm` object

    """

    if support_non_cryptographic_algorithms:
        try:
            return ZlibHashAlgorithm(hash_algorithm)
        except Exception:
            pass

    try:
        return OpenSSLHashAlgorithm(hash_algorithm)
    except Exception:
        pass


def _hash_file_content(args):
    # args = (filename, hash_algorithm)
    # helper function for multi threading of file hashing
    hasher = new_hash_instance(hash_algorithm=args[1],
                               support_non_cryptographic_algorithms=True)
    with open(args[0], 'rb') as f:
        for block in iter(lambda: f.read(64 * 1024), b''):
            hasher.update(block)

    return hasher.checksum, args[0]
