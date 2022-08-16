set term svg enhanced mouse size 1000,1000
# set term svg size 1000,1000
set output 'plots/summary_hits.svg'

set multiplot layout 1,1

sample_3_11(x)      = a0*x + b0
sample_direct_lru(x)= a1*x + b1
sample_main(x)      = a2*x + b2
sample_optimized_main(x)            = a3*x + b3
sample_optimized_direct_lru(x)      = a4*x + b4

# set decimalsign ','
set decimalsign locale
set format x "%'.0f"

set xlabel 'Cache size'
set ylabel 'Duration for 1,000,000 cache hits'

fit sample_3_11(x)       'benchmark-output/3_11' using 1:3 via a0,b0
fit sample_direct_lru(x) 'benchmark-output/direct_lru' using 1:3 via a1,b1
fit sample_main(x)       'benchmark-output/main' using 1:3 via a2,b2
fit sample_optimized_main(x)       'benchmark-output/optimized-main' using 1:3 via a3,b3
fit sample_optimized_direct_lru(x)       'benchmark-output/optimized-direct-lru' using 1:3 via a4,b4

# plot \
#     'benchmark-output/3_11' using 1:3, \
#     sample_3_11(x) lt 5, \

plot \
      'benchmark-output/optimized-main' using 1:3 \
    , sample_optimized_main(x) \
    , 'benchmark-output/optimized-direct-lru' using 1:3 \
    , sample_optimized_direct_lru(x) \


    # , 'benchmark-output/3_11' using 1:3 \
    # , sample_3_11(x) lt 5 \

    # 'benchmark-output/direct_lru' using 1:3 \
    # , sample_direct_lru(x) \
    # , 'benchmark-output/main' using 1:3 \
    # , sample_main(x) \
