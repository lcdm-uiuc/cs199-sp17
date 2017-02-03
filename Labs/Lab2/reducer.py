#!/usr/bin/env python

import sys

# We explicitly define the word/count separator token.
sep = '\t'

# We open STDIN and STDOUT
with sys.stdin as fin:
    with sys.stdout as fout:

        # Keep track of current word and count
        cword = None
        ccount = 0
        word = None

        # For every line in STDIN
        for line in fin:

            # Strip off leading and trailing whitespace
            # Note by construction, we should have no leading white space
            line = line.strip()

            # We split the line into a word and count, based on predefined
            # separator token.
            #
            # Note we haven't dealt with punctuation.

            word, scount = line.split('\t', 1)

            # We will assume count is always an integer value

            count = int(scount)

            # word is either repeated or new

            if cword == word:
                ccount += count
            else:
                # We have to handle first word explicitly
                if cword is not None:
                    fout.write("{0:s}{1:s}{2:d}\n".format(cword, sep, ccount))

                # New word, so reset variables
                cword = word
                ccount = count
        else:
            # Output final word count
            if cword == word:
                fout.write("{0:s}{1:s}{2:d}\n".format(word, sep, ccount))
