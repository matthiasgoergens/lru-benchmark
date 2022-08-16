import random
import functools as ft
import sys
import time
import pathlib as p
import gc
import argparse

output_dir = p.Path("benchmark-output")


def bench_hits_1(cachesize, reps):
    r = random.Random()
    r.seed(0)
    f = ft.lru_cache(maxsize=cachesize)(id)

    # fill cache at random:
    keys = list(range(cachesize))
    r.shuffle(keys)
    for k in keys:
        f(k)

    start = time.perf_counter()

    for c in range(reps):
        f(r.randrange(cachesize))
    end = time.perf_counter()
    return end - start


def bench_hits(output):
    with output.open("at") as o:
        reps = 1_000_000
        cachesize = random.randrange(100_000)
        t = bench_hits_1(cachesize=cachesize, reps=reps)
        o.write(f"{cachesize}\t{reps}\t{t}\n")


def main():
    output_dir.mkdir(exist_ok=True)
    output = output_dir / sys.argv[1]
    bench_hits(output)


if __name__ == "__main__":
    main()
