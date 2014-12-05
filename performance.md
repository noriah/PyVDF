Tests run on i7-2670QM 2.2GHz, 8GB DDR3

### Current Version
```Bash
$ python -d vdftest.py
         4415 function calls in 0.004 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003    0.004    0.004 PyVDF.py:73(parse)
     1176    0.001    0.000    0.001    0.000 {method 'match' of '_sre.SRE_Pattern' objects}
     1176    0.000    0.000    0.000    0.000 {method 'group' of '_sre.SRE_Match' objects}
     1177    0.000    0.000    0.000    0.000 {len}
      442    0.000    0.000    0.000    0.000 {method 'pop' of 'collections.deque' objects}
      442    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```


#### Old Versions

Less Overhead: e0610e0a77d09c9fb4f6ba4ee42dd7fee7dfd22b
```Bash
$ time python vdftest.py 
         889 function calls in 0.006 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.006    0.006    0.006    0.006 PyVDF.py:57(parse)
      442    0.000    0.000    0.000    0.000 {method 'pop' of 'list' objects}
      442    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'read' of 'file' objects}
        1    0.000    0.000    0.000    0.000 {open}
        1    0.000    0.000    0.000    0.000 {len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



real    0m0.041s
user    0m0.033s
sys 0m0.008s
```

Updated. Providing test material: 5ea8aae344f739db7461066ea7e3aa0f3e30202a
```Bash
$ time python vdftest.py 
         1625 function calls (1183 primitive calls) in 0.007 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.007    0.007 PyVDF.py:21(__init__)
        1    0.000    0.000    0.007    0.007 PyVDF.py:47(readArray)
    443/1    0.003    0.000    0.007    0.007 PyVDF.py:101(loop)
     1176    0.004    0.000    0.004    0.000 PyVDF.py:60(readToken)
        1    0.000    0.000    0.000    0.000 {method 'read' of 'file' objects}
        1    0.000    0.000    0.000    0.000 {open}
        1    0.000    0.000    0.000    0.000 {method 'close' of 'file' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



real    0m0.037s
user    0m0.032s
sys 0m0.010s
```