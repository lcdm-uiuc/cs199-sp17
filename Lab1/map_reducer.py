import multiprocessing
import itertools
from operator import itemgetter

NUM_WORKERS = 10


class MapReduce(object):
    def __init__(self, map_func, reduce_func):
        # Function for the map phase
        self.map_func = map_func

        # Function for the reduce phase
        self.reduce_func = reduce_func

        # Pool of processes to parallelize computation
        self.proccess_pool = multiprocessing.Pool(NUM_WORKERS)

    def kv_sort(self, mapped_values):
        return sorted(list(mapped_values), key=itemgetter(0))

    def __call__(self, data_in):
        # Run the map phase in our process pool
        map_phase = self.proccess_pool.map(self.map_func, data_in)

        # Sort the resulting mapped data
        sorted_map = self.kv_sort(itertools.chain(*map_phase))

        # Run our reduce function
        reduce_phase = self.reduce_func(sorted_map)

        # Return the results
        return reduce_phase
