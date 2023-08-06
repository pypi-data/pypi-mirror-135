import argparse
from rsm4dcm.rsm4dcm import rsm

def main():
    parser = parse_args()

    # handlers for parser
    func = None
    try:
        args = parser.parse_args()
        func = args.func
    except AttributeError:
        parser.print_help()
    if func is not None:
        args.func(args, parser)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        help="Path of the folder containing DICOM files (or subdirs with DICOM files)",
        required=True)

    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        help="Path of the folder where all DICOM files found will be moved",
        required=True)
    parser.set_defaults(func=do_rsm)
    return parser

def do_rsm(args, *other):
    """handler for rsm function"""
    rsm(args.target, args.outdir)

if __name__ == '__main__':
    main()
