"""Run the koans in curriculum order, stopping at the first failure."""

import argparse
import sys
import unittest

from checks import TRACKS, suite


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("track", nargs="?", choices=TRACKS)
    parser.add_argument("module", nargs="?", help="Run one module within a track")
    args = parser.parse_args(argv)
    if args.module and args.module not in TRACKS[args.track]:
        parser.error(f"choose a module from {', '.join(TRACKS[args.track])}")
    try:
        # Run lazily so a syntax error in a later file cannot hide today's koan.
        def run(result):
            for case in suite(args.track, args.module):
                case(result)
                if result.shouldStop:
                    break

        result = unittest.TextTestRunner(verbosity=2, failfast=True).run(run)
    except (SyntaxError, ImportError) as error:
        print(f"Could not load a koan: {error}", file=sys.stderr)
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
