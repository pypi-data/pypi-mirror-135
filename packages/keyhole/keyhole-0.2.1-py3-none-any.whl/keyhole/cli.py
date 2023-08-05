import argparse
import sys

from .mosaick import cli as mosaick_cli
from .register import cli as registration_cli


epilog = """\
Use the register subcommand to coregister panel scans and write the resulting
transforms to a file. Then use the mosaick subcommand to stitch the images
together into a single image according to the transforms from the previous
step.

Where you have four panels labeled name_a.tif through name_d.tif, this will
look like:

    $ keyhole register name_*.tif coreg.json
    $ keyhole mosaick coreg.json name_*.tif output.tif

'keyhole register -h' and 'keyhole mosaick -h' describe additional options.
"""


def main():
    cli(parse_args(sys.argv))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="keyhole: manipulate panel scans of Keyhole satellite imagery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )

    subparsers = parser.add_subparsers(
        title="subcommands", metavar="subcommand", required=True
    )

    parse_register = subparsers.add_parser("register", help="coregister images")
    parse_register.set_defaults(func=registration_cli.cli)
    registration_cli.config_parser(parse_register)

    parse_mosaick = subparsers.add_parser("mosaick", help="mosaick images")
    parse_mosaick.set_defaults(func=mosaick_cli.cli)
    mosaick_cli.config_parser(parse_mosaick)

    return parser.parse_args(argv[1:])


def cli(args):
    args.func(args)
