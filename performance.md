### New Version
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


### Old Version
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