# Gravitum

Gravitum is a toolkit for restoring reversed program with Python.

## Requirements

- Python 3.6+

## Installation

```
$ pip install gravitum
```

## Example

First, Gravitum defines some int types (`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`). They based on the int types of [numpy](https://github.com/numpy/numpy), but have type conversion rules closer to C programs.

```python
from gravitum.types import int8, int16, uint8, uint32

v1 = uint8(1)
v2 = int8(2)
v3 = int16(3)

# uint8
print(type(v1 + 1))

# uint8
print(type(v1 + v2))

# int16
print(type(v1 + v3))

# cast type
v3 = uint32(v3)
# another way
v3 = uint32 == v3
```

Second, Gravitum provides  `VirtualPointer` to simulate pointer operation on  `bytearray` .

For a C program:

```c
unsigned __int8 v[12] = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12};
*((unsigned __int32 *)(v + 2) + 1) = 1;
```

You can write with Gravitum:

```python
from gravitum import VirtualPointer
from gravitum.types import uint8, uint32

v = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
p = VirtualPointer(v, int_type=uint8)
p.add(2).cast(uint32).add(1).write(1)
```

In addition, Gravitum also implemented some functions (`__ROR4__`, `__ROL4__`, `BYTE1`, `LOBYTE`, `HIBYTE`, etc.) which are used in the code decompiled by IDA. You can reference them from `gravitum.defs`.

```python
from gravitum.defs import __ROR4__
from gravitum.types import uint32

v = uint32(100)
v = __ROR4__(v, 8)
```

