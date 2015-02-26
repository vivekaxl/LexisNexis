#!/usr/bin/env python3

import gzip
import io
import sys

from Bio import SeqIO
from Bio import SeqUtils

if len(sys.argv) == 1:
    print("\nusage: {} [fa|fa.gz ...]\n".format(sys.argv[0]))
    sys.exit(2)


for file in sys.argv[1:]:

    fh = gzip.open(file, 'rt') if file.endswith('.gz') else open(file,'r')

    for record in SeqIO.parse(fh,'fasta'):
        # print(record)
        seq = record.seq
        print(">{}\n{}".format(record.description, seq))
        print("GC:{:.2f}".format(SeqUtils.GC(seq)))
    fh.close()