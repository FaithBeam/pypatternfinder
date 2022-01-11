# pypatternfinder

A Python 3 port of mrexodia's [PatternFinder](https://github.com/mrexodia/PatternFinder).

Signature matcher/wildcard pattern finder.

## Install

```pip install pypatternfinder```

## Usage

```python
from pypatternfinder import pattern

transform = pattern.transform("456?89?B")
data = bytearray([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])
result, offset = pattern.find(data, transform)
if result:
    print(offset)
```
