# set term svg enhanced mouse size 1000,3000
set term svg size 1000,3000
set output 'plots/summary.svg'

lru_3_11(x)      = a0*x + b0
lru_direct(x)= a1*x + b1
lru_main(x)      = a2*x + b2
lru_optimized_main(x)        = a3*x + b3
lru_optimized_direct(x)      = a4*x + b4

lru_optimized_main_misses(x)        = a5*x + b5
lru_optimized_direct_misses(x)      = a6*x + b6

lru_optimized_main_mixed(x)        = a7*x + b7
lru_optimized_direct_mixed(x)      = a8*x + b8

# set decimalsign ','
set decimalsign locale
set format x "%'.0f"

set xlabel 'Cache size'
set yrange [0:]

fit lru_3_11(x)       'benchmark-output/3_11' using 1:3 via a0,b0
fit lru_direct(x) 'benchmark-output/direct_lru' using 1:3 via a1,b1
fit lru_main(x)       'benchmark-output/main' using 1:3 via a2,b2
fit lru_optimized_main(x)       'benchmark-output/optimized-main' using 1:3 via a3,b3
fit lru_optimized_direct(x)       'benchmark-output/optimized-direct-lru' using 1:3 via a4,b4
fit lru_optimized_main_misses(x)       'benchmark-output/optimized-main-misses' using 1:3 via a5,b5
fit lru_optimized_direct_misses(x)       'benchmark-output/optimized-direct-lru-misses' using 1:3 via a6,b6

fit lru_optimized_main_mixed(x)       'benchmark-output/optimized-main-0_5' using 1:3 via a7,b7
fit lru_optimized_direct_mixed(x)       'benchmark-output/optimized-direct-lru-0_5' using 1:3 via a8,b8

# plot \
#     'benchmark-output/3_11' using 1:3, \
#     lru_3_11(x) lt 5, \

set multiplot layout 3,1
set ylabel 'Duration for 1,000,000 cache hits'
plot \
      'benchmark-output/optimized-main' using 1:3 \
    , lru_optimized_main(x) \
    , 'benchmark-output/optimized-direct-lru' using 1:3 \
    , lru_optimized_direct(x) \


    # , 'benchmark-output/3_11' using 1:3 \
    # , lru_3_11(x) lt 5 \

    # 'benchmark-output/direct_lru' using 1:3 \
    # , lru_direct_lru(x) \
    # , 'benchmark-output/main' using 1:3 \
    # , lru_main(x) \

set ylabel 'Duration for 1,000,000 cache misses'
plot \
      'benchmark-output/optimized-main-misses' using 1:3 \
      , lru_optimized_main_misses(x) \
      , 'benchmark-output/optimized-direct-lru-misses' using 1:3 \
      , lru_optimized_direct_misses(x) \

set ylabel 'Duration for 1,000,000 cache hits/misses'
plot \
        'benchmark-output/optimized-main-0_5' using 1:3 \
      , lru_optimized_main_mixed(x) \
      , 'benchmark-output/optimized-direct-lru-0_5' using 1:3 \
      , lru_optimized_direct_mixed(x) \
