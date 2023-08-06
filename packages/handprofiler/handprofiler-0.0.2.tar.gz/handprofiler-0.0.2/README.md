# Hand profiler

## Install

```bash
$ pip install handprofiler
```

## Example of use

```python
from time import sleep
from random import random

from handprofiler import Profiler

@Profiler.track('foo')
def foo():
    for _ in range(2):
        token = Profiler.start('in foo')
        sleep(random())
        Profiler.stop(token)

@Profiler.track('bar')
def bar():
    for _ in range(3):
        sleep(0.3+random()*0.001)

def zoo():
    for _ in range(4):
        token = Profiler.start('in zoo')
        sleep(random()*3)
        Profiler.stop(token)


bar()
zoo()
foo()
foo()

Profiler.printstats()
Profiler.clear()
```

```
total=0:00:01.772223 avg=0:00:00.443055±0:00:00.316111 runs=4                    in zoo
total=0:00:01.768178 avg=0:00:00.884089±0:00:00.006843 runs=2                    foo
total=0:00:01.766944 avg=0:00:00.441736±0:00:00.247907 runs=4                    in foo
total=0:00:00.902467 avg=0:00:00.902467±0:00:00 runs=1                           bar
```
