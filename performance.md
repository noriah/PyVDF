### New Version
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


### Old Version
```Bash
$ time python vdftest.py 
         4271 function calls (3826 primitive calls) in 0.007 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    0.007    0.007 PyVDF.py:21(__init__)
    443/1    0.003    0.000    0.006    0.006 PyVDF.py:49(readArray)
     1176    0.003    0.000    0.003    0.000 PyVDF.py:67(readToken)
        1    0.000    0.000    0.000    0.000 re.py:144(sub)
     1251    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        1    0.000    0.000    0.000    0.000 re.py:226(_compile)
        1    0.000    0.000    0.000    0.000 sre_compile.py:493(compile)
     1251    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
        1    0.000    0.000    0.000    0.000 sre_parse.py:675(parse)
        1    0.000    0.000    0.000    0.000 sre_compile.py:478(_code)
        1    0.000    0.000    0.000    0.000 sre_parse.py:301(_parse_sub)
        1    0.000    0.000    0.000    0.000 sre_parse.py:379(_parse)
        1    0.000    0.000    0.000    0.000 sre_compile.py:359(_compile_info)
        1    0.000    0.000    0.000    0.000 {method 'sub' of '_sre.SRE_Pattern' objects}
      2/1    0.000    0.000    0.000    0.000 sre_compile.py:32(_compile)
      3/2    0.000    0.000    0.000    0.000 sre_parse.py:140(getwidth)
        9    0.000    0.000    0.000    0.000 sre_parse.py:182(__next)
        8    0.000    0.000    0.000    0.000 sre_parse.py:201(get)
        6    0.000    0.000    0.000    0.000 sre_parse.py:130(__getitem__)
        1    0.000    0.000    0.000    0.000 {open}
    34/33    0.000    0.000    0.000    0.000 {len}
        1    0.000    0.000    0.000    0.000 {method 'close' of 'file' objects}
        1    0.000    0.000    0.000    0.000 sre_parse.py:178(__init__)
        5    0.000    0.000    0.000    0.000 sre_parse.py:138(append)
       32    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        9    0.000    0.000    0.000    0.000 {isinstance}
        1    0.000    0.000    0.000    0.000 sre_compile.py:354(_simple)
        4    0.000    0.000    0.000    0.000 {min}
        1    0.000    0.000    0.000    0.000 {_sre.compile}
        2    0.000    0.000    0.000    0.000 sre_compile.py:472(isstring)
        2    0.000    0.000    0.000    0.000 sre_parse.py:90(__init__)
        4    0.000    0.000    0.000    0.000 sre_parse.py:126(__len__)
        1    0.000    0.000    0.000    0.000 PyVDF.py:45(useFastDict)
        2    0.000    0.000    0.000    0.000 sre_parse.py:195(match)
        1    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 sre_parse.py:134(__setitem__)
        1    0.000    0.000    0.000    0.000 sre_parse.py:67(__init__)
        2    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
        4    0.000    0.000    0.000    0.000 {ord}
        1    0.000    0.000    0.000    0.000 {iter}
        1    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



real	0m0.041s
user	0m0.032s
sys	0m0.008s
```