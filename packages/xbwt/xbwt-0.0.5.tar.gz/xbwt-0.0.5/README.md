# XBWT
[![PyPI version](https://badge.fury.io/py/xbwt.svg)](https://pypi.org/project/xbwt/)

This library allows to compute the xbwt transform. The following link refers to the article in which it was defined: https://www.semanticscholar.org/paper/Compressing-and-indexing-labeled-trees%2C-with-Ferragina-Luccio/8c4f49913e8db00dc09c31af480bf4dc37a853d9.

## Documentation

https://htmlpreview.github.io/?https://github.com/dolce95/xbw-transform/blob/main/doc/xbwt.html

## Installation

```bash
pip install xbwt
```

## Usage from Python as a module
It is possible to use `xbwt` directly in a python script by import it.

```python
import xbwt

xbwt_obj = xbwt.readAndImportTree(r'C:\Users\dolce\OneDrive\Desktop\tree.txt')
xbwt = xbwt_obj.computeXBWT()
xbwt_obj.printXBWT(xbwt)

"""
*** XBW TRANSFORM OF THE TREE T *** 

[S_LAST, S_ALPHA]

[0, ['A', 0]]
[0, ['C', 0]]
[0, ['D', 0]]
[1, ['D', 0]]
[1, ['a', 1]]
[1, ['a', 1]]
[1, ['c', 1]]
[0, ['C', 0]]
[0, ['a', 1]]
[1, ['B', 0]]
[1, ['b', 1]]
[1, ['E', 0]]
[0, ['B', 0]]
[0, ['a', 1]]
[1, ['B', 0]]
[1, ['c', 1]]
"""
```

## Input format

The trees to be imported to build the xbw transform must comply with the format below. In particular, nodes must be specified through the [NODE] ... [\NODE] tag. It is important that the root node has the identifier "root" in its definition. Instead, the edges are specified via the [EDGE] ... [\EDGES] tag. In the latter case, for each node it is necessary to insert the respective nodes with which the edge is formed in the respective order.

```
[NODES]
root = 'label1'
n1 = 'label2'
n2 = 'label3'
n3 = 'label4'
n4 = 'label5'
[\NODES]

[EDGES]
root = [n1, n2]
n1 = [n3, n5]
[\EDGES]
```

