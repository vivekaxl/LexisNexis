#!/usr/bin/env python3

import gzip
import io
import sys
from numpy import *

from Bio import SeqIO

if len(sys.argv) == 1:
    print("\nusage: {} [fq|fq.gz ...]\n".format(sys.argv[0]))
    sys.exit(2)


for file in sys.argv[1:]:

    fh = gzip.open(file, 'rt') if file.endswith('.gz') else open(file,'r')

    for record in SeqIO.parse(fh,'fastq'):
        qual = record.letter_annotations['phred_quality']
        seq = record.seq

        print(record.id)
        print(seq)
        print('_'.join([str(x) for x in qual]))

        # length = len(seq)

        # for s,q in zip(seq,qual):
        #    print(s,q)


    fh.close()