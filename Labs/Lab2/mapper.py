#!/usr/bin/env python

# These examples are based off the blog post by Michale Noll:
#
# http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
#

import sys

# We explicitly define the word/count separator token.
sep = '\t'

# We open STDIN and STDOUT
with sys.stdin as fin:
    with sys.stdout as fout:

        # For every line in STDIN
        for line in fin:

            # Strip off leading and trailing whitespace
            line = line.strip()

            # We split the line into word tokens. Use whitespace to split.
            # Note we don't deal with punctuation.

            words = line.split()

            # Now loop through all words in the line and output

            for word in words:
                fout.write("{0}{1}1\n".format(word, sep))
