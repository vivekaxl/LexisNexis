#!/usr/bin/env python3

import stat
import os
import sys
import tempfile
import shutil

p = '/asb/qwer/seq.fa.gz'
p2 = '/abc/efg'

print(os.path.exists(p))
print(os.path.dirname((p)))
print(os.path.basename(p))
print(os.path.split(p))
print(os.path.splitext(p))
print(os.path.splitext(p2))
print(os.path.exists(p) and os.path.isdir(p))
print(os.path.exists(p) and os.path.isfile(p))
print('join:', os.path.join(p2, p))

p3 = '/asdf/../ac/./'
print(p3, ',', os.path.normpath(p3))

# list dir and grep
# filter
print( list(filter(lambda x: not x.startswith('.'), os.listdir(os.path.expanduser('~')))))

# make and remove dir
d = 'tmp'
if os.path.exists(d):
    shutil.rmtree(d)

os.mkdir(d)
os.mkdir(os.path.join(d,d))
# create a empty file
open(os.path.join(d, 'file'),'a').close()

def walktree(top, callback):
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if stat.S_ISDIR(mode):
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            callback(pathname)
        else:
            print('Skipping %s' % pathname)


def visitfile(file):
    print('visiting', file)

# walktree(os.path.expanduser('.'), visitfile)


# tmpfile

tmpdir = tempfile.mkdtemp(prefix='tmp_', suffix='.tmp', dir='./')  # dir
print(tmpdir)
print(os.path.isdir(tmpdir))
tmpdir2 = tempfile.mkdtemp(prefix='tmp_', suffix='.tmp', dir=tmpdir)

os.removedirs(tmpdir2)

(tfile, fh) = tempfile.mkstemp(prefix='tmp_', suffix='.tmp', dir='./')  # file
print(tfile)

print(os.path.isfile(tfile))