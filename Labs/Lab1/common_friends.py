from map_reducer import MapReduce


def friend_mapper(line):
    pass


def friend_reducer(friend_tuples):
    pass

if __name__ == '__main__':
    with open('friend_graph.txt') as f:
        lines = f.readlines()
    mr = MapReduce(friend_mapper, friend_reducer)
    common_friends = mr(lines)
    for relationship, friends in common_friends:
        print '{}\t{}'.format(relationship, friends)
