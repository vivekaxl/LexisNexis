#!/usr/bin/env python3

import os
import io
import sys
import logging

print(os.name)

print(os.environ)
print(os.environ['HOME'])

print(os.getcwd())

print(os.getenv('TMPDIR', default=None))

print(os.uname())

print("error", file=sys.stderr)


with open(sys.argv[0], 'r') as fh:
    for line in fh:
        pass
        # print(line, end='')
# logging
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("some information")
logging.warning("warning")
logging.error(("error!!!!"))
logging.critical("CRITICAL")