# Hand profiler

## Install

```bash
$ pip install handprofiler
```

## Example of use

```python
from time import sleep
from random import random

import handprofiler as  profiler


@profiler.track("foo")
def foo():
    for _ in range(2):
        token = profiler.start("in foo")
        sleep(random())
        profiler.stop(token)


@profiler.track("bar")
def bar():
    for _ in range(3):
        sleep(0.3 + random() * 0.001)


def zoo():
    for _ in range(4):
        token = profiler.start("in zoo")
        sleep(random() * 3)
        profiler.stop(token)


bar()
zoo()
foo()
foo()

profiler.printstats()
profiler.clear()
```

```
total=0:00:01.866119 avg=0:00:00.466529±0:00:00.340207 runs=4                    in foo
total=0:00:01.579377 avg=0:00:00.394844±0:00:00.310193 runs=4                    in zoo
total=0:00:00.902268 avg=0:00:00.902268±0:00:00 runs=1                           bar
total=0:00:00.867672 avg=0:00:00.433836±0:00:00.332681 runs=2                    foo
```
