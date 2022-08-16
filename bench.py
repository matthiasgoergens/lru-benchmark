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

def bench_miss(cachesize, reps):
    f = ft.lru_cache(maxsize=cachesize)(id)

    for k in range(cachesize):
        f(object())

    start = time.perf_counter()

    for c in range(reps):
        f(object())
    end = time.perf_counter()
    return end - start

def bench(output, which):
      while True:
        with output.open("at") as o:
          reps = 1_000_000
          cachesize = random.randrange(100_000)
          t = which(cachesize=cachesize, reps=reps)
          line = f"{cachesize}\t{reps}\t{t}\n"
          o.write(line)
          sys.stdout.write(line)


def main():
    output_dir.mkdir(exist_ok=True)
    output = output_dir / sys.argv[1]
    try:
      kind = sys.argv[2]
    except IndexError:
      kind = 'hits'
    print(kind)
    match kind:
      case 'hits':
          bench(output, which = bench_hits_1)
      case 'misses':
          bench(output, which = bench_miss)



if __name__ == "__main__":
    main()
