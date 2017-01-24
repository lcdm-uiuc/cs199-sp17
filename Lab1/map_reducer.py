import multiprocessing
from operator import itemgetter
from functools import reduce


NUM_WORKERS = 5

class MapReduce(object):
    def __init__(self, map_func, reduce_func):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.proccess_pool = multiprocessing.Pool(NUM_WORKERS)

    def kv_sort(self, mapped_values):
        return sorted(mapped_values, key=itemgetter(0))

    def __call__(self, data_in):
        print self.map_func
        map_phase = self.proccess_pool.map(self.map_func, data_in)
        sorted_map = self.kv_sort(map_phase)
        reduce_phase = self.proccess_pool.map(self.reduce_func, sorted_map)
        return reduce_phase
