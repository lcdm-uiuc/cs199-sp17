from map_reducer import MapReduce
from operator import itemgetter
from utils import strip_punctuation


def string_to_words(str_in):
    words = []
    # Split string into words
    for word in str_in.strip().split():
        # Strip punctuation
        word = strip_punctuation(word)

        # Note each individual instance of a word
        words.append((word, 1))
    return words


def word_count_reducer(word_tuples):
    # Dict to count the instances of each word
    words = {}

    for entry in word_tuples:
        word, count = entry

        # Add 1 to our word counts for each word we see
        if word in words:
            words[word] += 1
        else:
            words[word] = 1

    return words.items()

if __name__ == '__main__':
    with open('sherlock.txt') as f:
        lines = f.readlines()

    # Construct our MapReducer
    mr = MapReduce(string_to_words, word_count_reducer)
    # Call MapReduce on our input set
    word_counts = mr(lines)
    sorted_wc = sorted(word_counts, key=itemgetter(1), reverse=True)
    for word, count in sorted_wc[:100]:
        print '{}\t{}'.format(word, count)
