from map_reducer import MapReduce
from operator import itemgetter


def bigram_mapper(line):
    pass


def bigram_reducer(bigram_tuples):
    pass

if __name__ == '__main__':
    with open('sherlock.txt') as f:
        lines = f.readlines()
    mr = MapReduce(bigram_mapper, bigram_reducer)
    bigram_counts = mr(lines)
    sorted_bgc = sorted(bigram_counts, key=itemgetter(1), reverse=True)
    for word, count in sorted_bgc[:100]:
        print '{}\t{}'.format(word, count)
