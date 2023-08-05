"""Data Intergrity Fingerprint (DIF) command line interface.

Invoke with `python3 -m dataintegrityfingerprint` or
`dataintegrityfingerprint`.

"""


import os
import sys
import argparse

from . import DataIntegrityFingerprint
from . import __version__


def cli():

    def progress(count, total, status=''):
        bar_len = 50
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + ' ' * (bar_len - filled_len)
        sys.stdout.write('{:5.1f}% [{}] {}\r'.format(percents, bar, status))
        sys.stdout.flush()

    parser = argparse.ArgumentParser(
        description="""Data Integrity Fingerprint (DIF) - A reference implementation in Python
Version: v{0}""".format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Authors:
Oliver Lindemann <oliver@expyriment.org>
Florian Krause <florian@expyriment.org""")

    parser.add_argument("PATH", nargs='?', default=None,
                        help="the path to the data directory")
    parser.add_argument("-f", "--from-checksums-file",
                        dest="fromchecksumsfile", action="store_true",
                        help="Calculate dif from checksums file. " +
                             "PATH is a checksums file",
                        default=False)
    parser.add_argument("-a", "--algorithm", metavar="ALGORITHM",
                        type=str,
                        help="the hash algorithm to be used (default=SHA-256)",
                        default="sha256")
    parser.add_argument("-C", "--checksums", dest="checksums",
                        action="store_true",
                        help="print checksums only",
                        default=False)
    parser.add_argument("-D", "--dif-only", dest="difonly",
                        action="store_true",
                        help="print dif only",
                        default=False)
    parser.add_argument("-G", "--gui", dest="gui",
                        action="store_true",
                        help="open graphical user interface",
                        default=False)
    parser.add_argument("-L", "--list-available-algorithms", dest="listalgos",
                        action="store_true",
                        help="print available algorithms",
                        default=False)
    parser.add_argument("-s", "--save-checksums-file",
                        dest="savechecksumsfile", action="store_true",
                        help="save checksums to file",
                        default=False)
    parser.add_argument("-d", "--diff-checksums-file", metavar="CHECKSUMSFILE",
                        type=str,
                        help="Calculate differences of checksums to " +
                             "CHECKSUMSFILE")
    parser.add_argument("-n", "--no-multi-processing", dest="nomultiprocess",
                        action="store_true",
                        help="switch of multi processing",
                        default="")
    parser.add_argument("-p", "--progress", dest="progressbar",
                        action="store_true",
                        help="show progressbar",
                        default=False)
    parser.add_argument("--non-cryptographic",
                        dest="noncrypto",
                        action="store_true",
                        help="allow non cryptographic algorithms " +
                             "(Not suggested, please read documentation " +
                             "carefully!)",
                        default=False)

    args = vars(parser.parse_args())

    if args['listalgos']:
        print("Crypotographic algorithms")
        print("- " + "\n- ".join(
            DataIntegrityFingerprint.CRYPTOGRAPHIC_ALGORITHMS))
        if args['noncrypto']:
            print("Non-crypotographic algorithms")
            print("- " + "\n- ".join(
                DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS))
        sys.exit()

    if args['gui']:
        from .gui import start_gui
        start_gui(data_dir=args["PATH"], hash_algorithm=args["algorithm"])
        sys.exit()

    if args["PATH"] is None:
        print("Use -G to launch the GUI or -h for details about command line interface")
        sys.exit()

    dif = DataIntegrityFingerprint(
        data=args["PATH"],
        from_checksums_file=args['fromchecksumsfile'],
        hash_algorithm=args["algorithm"],
        multiprocessing=not(args['nomultiprocess']),
        allow_non_cryptographic_algorithms=args['noncrypto'])

    if not args['fromchecksumsfile'] and args['progressbar']:
        dif.generate(progress=progress)
        print("")

    # Output
    if args['savechecksumsfile']:
        extension = "".join(
            x for x in dif._hash_algorithm.lower() if x.isalnum())
        outfile = os.path.split( dif.data)[-1] + ".{0}".format(extension)
        answer = "y"
        if os.path.exists(outfile):
            answer = input(
                "'{0}' already exists! Overwrite? [y/N]: ".format(outfile))
        if answer == "y":
            dif.save_checksums()
            print("Checksums have been written to '{0}'.".format(outfile))
        else:
            print("Checksums have NOT been written.")

    elif args['diff_checksums_file']:
        diff = dif.diff_checksums(args['diff_checksums_file'])
        if diff != "":
            print(diff)

    elif args['difonly']:
        print(dif)
    elif args['checksums']:
        print(dif.checksums.strip())
    else:
        print("Data Integrity Fingerprint (DIF)")
        print("")
        print("Directory: {0}".format(dif.data))
        print("Files: {0}".format(dif.file_count))
        print("Algorithm: {0}".format(dif.hash_algorithm))
        print("")
        print("DIF [{}]: {}".format(dif.hash_algorithm, dif))
