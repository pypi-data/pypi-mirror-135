# DSKit

DSKit (Data Science Kit) is a Python package that provides tools for solving simple Data Science routine problems.

# Installing

```bash
pip install dskit
```

# Tutorial

DSKit consists of two submodules:

* *dskit.frame* - contains a set of functions for *pandas.DataFrame* and *pandas.Series* manipulation.
* *dskit.tensor* - contains a set of functions for *numpy.ndarray* manipulation.

## *dskit.frame*

### *dummifier*

*dummifier* is less harmful alternative to *pd.get_dummies*. This function takes a *Dict[str, Tuple[object, ...]]* and returns a *Callable[[pd.DataFrame], pd.DataFrame]* which takes a frame and returns a dummified frame. Key of the dictionary is treated as a name of a column and value of the dictionary is treated as a set of unique values of that column. *dummifier* also takes an optional parameter *name* which has a type *Callable[[str, object], str]*. The *name* function takes a name of a column and a unique value of that column to produce a name of a column in a dummified frame. The default implementation of the *name* is: `lambda n, x: n + "_" + str(x)`. *dummifier* uses *encoder* function under the hood.

```python
xs = pd.DataFrame({"A": (1, 2, 2, 5, 5), "B": ("a", "a", "b", "c", "d")})

dummify = dummifier(dict(xs))
print(dummify(xs))

#    A_1  A_2  A_5  B_a  B_b  B_c  B_d
# 0  1.0  0.0  0.0  1.0  0.0  0.0  0.0
# 1  0.0  1.0  0.0  1.0  0.0  0.0  0.0
# 2  0.0  1.0  0.0  0.0  1.0  0.0  0.0
# 3  0.0  0.0  1.0  0.0  0.0  1.0  0.0
# 4  0.0  0.0  1.0  0.0  0.0  0.0  1.0

ys = pd.DataFrame({"C": (True, True, False, True), "A": (1, 2, 3, 4)})
print(dummify(ys))

#        C  A_1  A_2  A_5
# 0   True  1.0  0.0  0.0
# 1   True  0.0  1.0  0.0
# 2  False  0.0  0.0  0.0
# 3   True  0.0  0.0  0.0
```

One of the reasons why *dummifier* is less harmful than *pd.get_dummies* is that it will not dummify new values. Thanks to that Machine Learning models will operate on data with the same number of dimensions regardless of new values presence in a new portion of data.

```python
old_frame = pd.DataFrame({"B": ("a", "a", "b")})
dummify = dummifier(dict(old_frame))

new_frame = pd.DataFrame({"B": ("a", "b", "c")})
print(dummify(new_frame))

#    B_a  B_b
# 0  1.0  0.0
# 1  0.0  1.0
# 2  0.0  0.0

print(pd.get_dummies(new_frame))

#    B_a  B_b  B_c
# 0    1    0    0
# 1    0    1    0
# 2    0    0    1
```

### *encoder*

*encoder* is a function which takes a set of values and returns a *Callable[[Tuple[object, ...]], pd.DataFrame]*. The returned function one-hot-encodes passed values. *encoder* also takes an optional parameter *name* which has a type *Callable[[object], str]*. The *name* function takes a unique value from the passed set to produce a name of a column in a one-hot-encoded frame. The default implementation of the *name* is: `str`. This function uses *sklearn.preprocessing.OneHotEncoder* under the hood.

```python
encoded = encoder((1, 2, 3))((1, 2, 3, 4, np.nan))
print(encoded)

#      1    2    3
# 0  1.0  0.0  0.0
# 1  0.0  1.0  0.0
# 2  0.0  0.0  1.0
# 3  0.0  0.0  0.0
# 4  0.0  0.0  0.0

encoded = encoder((1, 2, 3), name=lambda x: "column_" + str(x))((1, 2, 3, 4, np.nan))
print(encoded)

#    column_1  column_2  column_3
# 0       1.0       0.0       0.0
# 1       0.0       1.0       0.0
# 2       0.0       0.0       1.0
# 3       0.0       0.0       0.0
# 4       0.0       0.0       0.0
```

## *dskit.tensor*

### *batch*

*batch* is a function which takes a *Tuple[Tuple[np.ndarray, ...], ...]*, transposes it and applies *np.stack* on each element resulting in a *Tuple[np.ndarray, ...]*.

```python
xs = (
  (np.array([1, 2, 3]), np.array([4, 5]), np.ones((2, 3))),
  (np.array([7, 8, 9]), np.array([5, 4]), np.zeros((2, 3)))
)

x, y, z = batch(xs)

print(x)
print("=" * 5)
print(y)
print("=" * 5)
print(z)

# [[1 2 3]
#  [7 8 9]]
# =====
# [[4 5]
#  [5 4]]
# =====
# [[[1. 1. 1.]
#   [1. 1. 1.]]
#
#  [[0. 0. 0.]
#   [0. 0. 0.]]]
```

### *batches*

*batches* is a function which takes a sliding window length **n** and a **step**, and returns a function which takes an *Iterable[Tuple[np.ndarray, ...]]*, applies sliding window over it and uses *batch* function on each window. This function returns an *Iterable[Tuple[np.ndarray, ...]]*. Each window has length equal to **n**. In case when **exact=False** option is passed, each window has at most length equal to **n**. **step** is simply a shift of a sliding window. By default **step** is equal to **n**.

```python
xs = np.arange(15).reshape(-1, 3)
ys = np.arange(10).reshape(-1, 2)

print(xs)

# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]

print(ys)

# [[0 1]
#  [2 3]
#  [4 5]
#  [6 7]
#  [8 9]]

for x, y in batches(n=3)(zip(xs, ys)):
  print(x)
  print("=" * 5)
  print(y)

  print()

# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
# =====
# [[0 1]
#  [2 3]
#  [4 5]]
#

for x, y in batches(n=3, step=2, exact=False)(zip(xs, ys)):
  print(x)
  print("=" * 5)
  print(y)

  print()

# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
# =====
# [[0 1]
#  [2 3]
#  [4 5]]
#
# [[ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]
# =====
# [[4 5]
#  [6 7]
#  [8 9]]
#
# [[12 13 14]]
# =====
# [[8 9]]
#
```

### *cycle*

*cycle* is a multidimensional version of *itertools.cycle* function. This function takes a *np.ndarray* with *Tuple[int, ...]* and returns "cycled" *np.ndarray*.

```python
xs = np.arange(4).reshape(-1, 2)
print(xs)

# [[0 1]
#  [2 3]]

cycled_xs = cycle(xs, (3, 3))
print(cycled_xs)

# [[0 1 0 1 0 1]
#  [2 3 2 3 2 3]
#  [0 1 0 1 0 1]
#  [2 3 2 3 2 3]
#  [0 1 0 1 0 1]
#  [2 3 2 3 2 3]]

zeros = cycle(0, (2, 2, 3))
print(zeros)

# [[[0 0 0]
#   [0 0 0]]
#
#  [[0 0 0]
#   [0 0 0]]]
```

### *gridrange*

*gridrange* is a function similar to Python's *range* function. The difference between *gridrange* and *range* is that *gridrange* operates on *Tuple[int, ...]* instead of *int*.

```python
for x in gridrange((2, 3)):
  print(x)

# (0, 0)
# (0, 1)
# (0, 2)
# (1, 0)
# (1, 1)
# (1, 2)

for x in gridrange((1, 1), (3, 4)):
  print(x)

# (1, 1)
# (1, 2)
# (1, 3)
# (2, 1)
# (2, 2)
# (2, 3)

for x in gridrange((1, 1), (10, 20), (5, 5)):
  print(x)

# (1, 1)
# (1, 6)
# (1, 11)
# (1, 16)
# (6, 1)
# (6, 6)
# (6, 11)
# (6, 16)
```

### *iteraxis*

*iteraxis* is a function which takes a *np.ndarray* and returns *Iterable[np.ndarray]* along passed axis. This function is similar to *np.apply_along_axis*. The difference between *iteraxis* and *np.apply_along_axis* is that *np.apply_along_axis* applies some function to arrays, when *iteraxis* returns those arrays.

```python
xs = np.arange(27).reshape(-1, 3, 3)

for x in iteraxis(xs, axis=-1):
  print(x)

# [0 1 2]
# [3 4 5]
# [6 7 8]
# [ 9 10 11]
# [12 13 14]
# [15 16 17]
# [18 19 20]
# [21 22 23]
# [24 25 26]
```

### *move*

*move* allows you to move source *np.ndarray* to destination *np.ndarray* at coordinate *Tuple[int, ...]*. *move* works on a copy of the *destination* array unless *inplace=True* is passed. The default coordinate is *(0, 0, ...)*.

```python
xs = np.arange(4).reshape(-1, 2)
ys = np.zeros((3, 3), dtype=np.uint)

moved = move(xs, ys, coordinate=(1, 1))
print(moved)

# [[0 0 0]
#  [0 0 1]
#  [0 2 3]]

xs = np.arange(4).reshape(-1, 2)
ys = np.zeros((3, 3), dtype=np.uint)

_ = move(xs, ys, inplace=True)
print(ys)

# [[0 1 0]
#  [2 3 0]
#  [0 0 0]]
```

### *slices*

*slices* is simply:

```python
RawSlice = Union[
  Tuple[Optional[int]],
  Tuple[Optional[int], Optional[int]],
  Tuple[Optional[int], Optional[int], Optional[int]]
]

def slices(xs: Iterable[RawSlice]) -> Tuple[slice, ...]:
  return tuple(starmap(slice, xs))
```

Example of *slices* usage:

```python
xs = np.arange(9).reshape(-1, 3)
ys = (1, None), (0, 1)

print(xs[slices(ys)])

# [[3]
#  [6]]

# same as

print(xs[1:, 0:1])

# [[3]
#  [6]
```
