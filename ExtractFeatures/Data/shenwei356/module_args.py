#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")

parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")

parser.add_argument("-f", "--flag", help="flag",
                    action="store_true")

parser.add_argument("-t", "--type", help="type [1, 2, 3]",
                    type=int, choices=[1, 2, 3])

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help="flag",
                    action="count", default=0)
group.add_argument("-q", "--quiet", action="store_true")



args = parser.parse_args()

answer = args.x ** args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))