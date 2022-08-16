import random
import functools as ft
import sys
import time
import pathlib as p
import gc

# test lru.
output_dir = p.Path('benchmark-output-old')

reps = 400_000 # 10 * cachesize

def bench1(cachesize, hits, file='vanillaconf_dictlru.data'):
    try:
        gc.disable()
        r = random.Random()
        r.seed(0)
        # random.seed(0)
        f = ft.lru_cache(maxsize=cachesize)(id)
        global_start = time.perf_counter()
        global_time = 0
        with (output_dir/file).open('at') as o:
            for c in range(reps):
                if hits == 1:
                    # i = c % cachesize
                    i = r.randrange(cachesize)
                elif hits == 0:
                    i = object()
                else:
                    i = r.randrange(round(cachesize/hits))
                local_start = time.perf_counter()
                f(i)
                stop = time.perf_counter()
                local_time = stop - local_start
                global_time += local_time
                o.write(f'{cachesize}\t{hits}\t{c}\t{local_time}\t{global_time}\t{i}\n')
    finally:
        gc.enable()

def bench():

    # cachesize=100_000
    # hits = 0.1

    while True:
        cachesize = random.randrange(100_000)
        # hits = random.choice([0, 0.5, 1])
        hits = random.random()
        print(f"{cachesize}\t{hits}\t", end='')
        sys.stdout.flush()
        start = time.perf_counter()
        bench1(cachesize, hits)
        stop = time.perf_counter()
        print(f"{stop - start}")
        with (output_dir/'vanillaconf_dictlru_summary.data').open('at') as o:
            o.write(f"{cachesize}\t{hits}\t{stop - start}\n")

def main():
    x = 0
    cachesize=100_000
    hits = 0.1
    reps = 10 * cachesize

    @ft.lru_cache(maxsize=cachesize)
    def f(i):
        nonlocal x
        x += 1
        return (i, x, object())
    random.seed(0)
    
    start = time.perf_counter()
    for c in range(reps):
        i = random.randrange(round(cachesize/hits))
        f(i)
        # print(f'{c} {i}: ', end='')
        # sys.stdout.flush()
        # print(f(i))
    stop = time.perf_counter()
    print(f"{cachesize},{reps},{stop - start}")

if __name__=='__main__':
    output_dir.mkdir(exist_ok=True)
    for _ in range(5):
        bench1(cachesize=20_0000, hits=1, file='single-hit-3.10-no-gc.data')
    # bench()
