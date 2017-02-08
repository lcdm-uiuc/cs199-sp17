import re
import string


def strip_punctuation(str_in):
    # Strip punctuation from word (don't worry too much about this)
    return re.sub('[%s]' % re.escape(string.punctuation), '', str_in)
