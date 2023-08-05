from delo import *
import numpy as np

def square(x):
    return np.sum(x ** 2, axis=1)
file_name = 'square_opt.log'
logger = PickleLogger(file=file_name)
described_function = DescribedFunction(square, dimension=2, domain_lower_limit=-10, domain_upper_limit=10)
algorithm = DElo(10, logger=logger)
algorithm.optimize(described_function, rng_seed=2022)
logreader = PickleLogReader(file_name)
best_fs = logreader.read_variable('current_best_f')
print(best_fs[0:5])