import time
import sys
import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
from numba import njit

if len(sys.argv) < 3:
    print("Please, specify juliacall, pyjulia or python and the number of processes to use")
    sys.exit()

N_DATA = 100
N_JOBS = int(sys.argv[2])


def julia_import(module: str, filename: str):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            # including stuffs
            if sys.argv[1] == 'juliacall':
                from juliacall import Main
            elif sys.argv[1] == 'pyjulia':
                from julia import Main
            if not hasattr(Main, module):
                Main.include(filename)

            return fn(Main, *args, **kwargs)
        return wrapper
    return decorator


@julia_import("MyModule", "lib.jl")
def python_function_using_julia(Main, *args, **kwargs):
    return Main.MyModule.julia_function(*args, **kwargs)


def python_function(arr):
    """
    This is a simple function that is aimed to run in parallel
    It does nothing meaningful, just sums stuffs in a way that cannot be done
    with a simple `sum()` function
    """
    s = 0
    H = arr.shape[1]
    for d in range(arr.shape[0]):
        for i in range(arr.shape[0]):
            for j in range(H):
                k = max(0, i - d)
                h = min(H-1, j + d)
                s += arr[i, j] + arr[k, h]
    return s


numba_function = njit(python_function)


def run_parallel(fn, method):
    data = [np.random.rand(1280, 700) for _ in range(N_DATA)]
    print("Testing " + method)
    try:
        ttt = time.time()
        # or max_nbytes=None if data are really big
        res = Parallel(n_jobs=N_JOBS, backend="loky", mmap_mode="w+")(
            delayed(fn)(arr) for arr in tqdm(data))
        print(sum(res))
        print(f"Needed time: {time.time() - ttt}")
    except Exception as e:
        print(method + " failed with exception:")
        print(e)


if __name__ == "__main__":
    if sys.argv[1] == 'python':
        fn = python_function
    elif sys.argv[1] == 'numba':
        fn = numba_function
    else:
        fn = python_function_using_julia
    run_parallel(fn, sys.argv[1])
