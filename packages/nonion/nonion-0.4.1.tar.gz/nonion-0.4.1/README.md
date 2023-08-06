# NOnion

NOnion is a Python package that provides tools for Functional Programming. One of its aims is to eliminate nested function calls such as **z(g(f(x)))** which remind an __onion__.

# Installing

```bash
pip install nonion
```

# Tutorial

NOnion contains a set of functions and types that __might__ simplify your workflow with Functional Programming in Python. Those tools are designed (but not limited) to work with *Function* and *Pipeline* wrappers.

* *Function* - a wrapper of **any** Python *Callable*,
* *Pipeline* - a wrapper of **any** Python *Iterable*.

It is important to understand that *NOnion* provides tools used for FP in context of Python. Because it is impossible to fully implement some constructs from FP languages in Python, *NOnion* provides tools that resemble some of those constructs.

## *Function*

In order to create a *Function*, you simply pass any *Callable*:

```python
f = Function(lambda x: x + 1)
f(5) # 6
```

You can also create an identity *Function*:

```python
g = Function()
```

Notice, that a *Function* takes exactly single value and returns exactly single value.

### *compose*

A ``Function composition" defined as $( f \circ g )(x) = f(g(x))$ could be done in the following way:

```python
z = f @ g

# alternatively

z = f.compose(g)
```

You can also use *compose* several times:

```python
z = f @ g @ f
```

Instead of wrapping each *Callable* with a *Function*, you can wrap only __first__ *Callable* and use *compose* on the rest.

```python
def f(x):
  return x + 1

g = Function() @ (lambda x: x * 2) @ f
g(5) # 12
```

### *then*

Function composition sometimes might be hard to read, because you have to read it from right-to-left.
In order to achieve better readability, you can use *then*.

```python
g = Function() / (lambda x: x * 2) / f
g(5) # 11

# alternatively

g = Function().then(lambda x: x * 2).then(f)
g(5) # 11
```

### *fanout*

If you need to pass an argument to two functions, you can use *fanout*:

```python
g = Function() / (lambda x: x + 1) & (lambda x: x * 2)
g(5) # (6, 10)

mean = (Function() / sum & len) / star(op.truediv)
mean([1, 2, 3]) # 2.0

# alternatively

g = Function().then(lambda x: x + 1).fanout(lambda x: x * 2)
g(5) # (6, 10)

mean = (Function().then(sum).fanout(len)).then(star(op.truediv))
mean([1, 2, 3]) # 2.0
```

### *split*

If you need to apply first value of a pair to a first function and a second value of the pair to a second function, you can use *split*:

```python
g = Function() / (lambda x: x + 1) ^ (lambda x: x * 2)
g((2, 3)) # (3, 6)

teams = {"team a": ["member 1", "member 2"], "team b": ["member 3"]}
f = Function() / str.capitalize ^ len
for t in teams.items():
  print(f(t))

# ('Team a', 2)
# ('Team b', 1)

# alternatively

g = Function().then(lambda x: x + 1).split(lambda x: x * 2)
g((2, 3)) # (3, 6)

f = Function().then(str.capitalize).split(len)
for t in teams.items():
  print(f(t))

# ('Team a', 2)
# ('Team b', 1)
```

### *call*

Sometimes you want to call a function ``inline'' after several compositions. In this case, you might use:

```python
(Function() / (lambda x: x * 2) / f)(5) # 11
```

But it might be hard to read. Especially, when you mostly pass lambdas. A better way to call a function is by using:

```python
Function() / (lambda x: x * 2) / f | 5 # 11
```

### *star* (function)

Suppose, that you defined a function with multiple arguments such as:

```python
def f(x, y):
  return x + y * x
```

And you want to wrap that function using Function. In this case, you have to use *star*.

```python
Function() @ star(f) | (1, 2) # 3
```

*star* simply passes arguments to a function using Python *\** (star) operator.

### *unstar* (function)

*unstar* is the opposite function to *star*:

```python
names = unstar(", ".join)("Haskell Curry", "John Smith", "George Sand")
print(names) # Haskell Curry, John Smith, George Sand
```

### *foreach*

You can also call a function for each value in some *Iterable* in the following way:

```python
ys = Function() / (lambda x: x * 2) / (lambda x: x + 1) * range(5)

for y in ys:
  print(y)

# 1
# 3
# 5
# 7
# 9
#
```

## *Pipeline*

In order to create a *Pipeline*, you simply pass any *Iterable*:

```python
xs = Pipeline(range(5))

# notation abuse, do not use that:

xs = Function() / Pipeline | range(5)
```

You can also create an empty *Pipeline*:

```python
xs = Pipeline()
```

Under the hood *Pipeline* is simply uses *iter* on a passed *Iterable*. It means, that if you will pass an *Iterable*, that could be exhausted, you iterate over *Pipeline* only once.

```python
xs = Pipeline(range(2))

for x in xs:
  print(x)

# 1
# 2
#

# perfectly fine, because range(x) returns a special object
for x in xs:
  print(x)

# 1
# 2
#

xs = Pipeline(x for x in range(2))

for x in xs:
  print(x)

# 1
# 2
#

# xs already exhausted
for x in xs:
  print(x)
```

### *map*

*map* allows you to call a *Callable*, which takes a single value and returns a single value, on each value of the *Pipeline*.

```python
ys = Pipeline(range(3)) / (lambda x: x + 1) / (lambda x: (x, x + 1)) / star(lambda x, y: x + y * x)

for y in ys:
  print(y)

# 3
# 8
# 15
#

# alternatively

ys = Pipeline(range(3)).map(lambda x: x + 1).map(lambda x: (x, x + 1)).map(star(lambda x, y: x + y * x))
```

### *filter*

*filter* allows you to filter *Pipeline* values.

```python
ys = Pipeline(range(3)) % (lambda x: x > 1)

for y in ys:
  print(y)

# 2
#

# alternatively

ys = Pipeline(range(3)).filter(lambda x: x > 1)
```

### *flatmap*

*flatmap* allows you to call a *Callable*, which takes a single value and returns an *Iterable*, on each value of the *Pipeline* and flatten results into single *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) * (lambda x: (x, x + 1))

for y in ys:
  print(y)

# 1
# 2
# 2
# 3
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).flatmap(lambda x: (x, x + 1))
```

### *apply*

*apply* allows you to call a *Callable*, which takes an *Iterable* and returns an *Iterable*, on whole *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) // tuple # internally Pipeline now has a tuple

for y in ys:
  print(y)

# 1
# 2
#

# now multiple itertations is possible
for y in ys:
  print(y)

# 1
# 2
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).apply(tuple)
```

### *collect*

*collect* allows you to call a *Callable*, which takes an *Iterable* and returns any single value, on whole *Pipeline*. The difference between *apply* and *collect* is that *collect* returns the result of a function instead of wrapping it with *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) >> tuple
print(ys)

# (1, 2)
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).collect(tuple)
```

You can also combine *collect* with any function which takes an *Iterator*:

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) >> next_
print(ys) # (1,)

ys = Pipeline(range(2)) % (lambda x: x == 5) >> next_
print(ys) # ()

ys = Pipeline(range(5)) >> shift(islice, 2)

for y in ys:
  print(y)

# 0
# 1

# alternatively you can use apply

ys = Pipeline(range(5)) // shift(islice, 2) | print

# 0
# 1
```

### *foreach*

*foreach* allows you to call a *Callable*, which takes a single value, on each value of the *Pipeline*.

```python
Pipeline(range(2)) / (lambda x: x + 1) | print

# 1
# 2
#

# alternatively

Pipeline(range(2)).map(lambda x: x + 1).foreach(print)
```

## *groupon*

*groupon* is a function which takes a function *Callable[[X], Y]*, and returns some function which takes *Iterable[X]* and returns *Iterable[X]* grouped on *Callable[[X], Y]* function. The *groupon* function uses Python *groupby* function under the hood. *groupon* adds a grouping key using passed *Callable[[X], Y]* function and sorts values by that key before applying *groupby*.

```python
xs = -3, 1, 0, -1, 5

(
  Pipeline(xs)
  // groupon(lambda x: x > 0)
  / value(tuple)
  | print
)

# (False, (-3, 0, -1))
# (True, (1, 5))
```

## *nonion.tools*

### *Either*

*Either* is a type alias. *Either* is defined as follows:

```python
Either = Tuple[Maybe[X], Maybe[Y]]
```

*Either* can be used when you need to return either left (bad) value or a right (good) value:

```python
def readline(path: str) -> Either[str, str]:
  h: Maybe[IOBase] = try_(open)(path)

  if not h:
    return (("error occurred during open",), ())

  h, *_ = h
  line = h.readline()
  h.close()

  return ((), line)

error, line = readline("requirements.txt")

if line:
  print(*line)
else:
  print(*error)
```

Because *Either* is simply a type alias, it does not checks whether only left or only right value is passed.

### *Maybe*

*Maybe* is a type alias. *Maybe* resembles Haskell's *Maybe* in Python. *Maybe* is defined as follows:

```python
Maybe = Union[Tuple[X], Tuple[()]]
```

As we can see *Maybe* is simply some *tuple* that might contain a single value or be an empty *tuple*.
It means that in order to initialize an *Maybe* you can simply write:

```python
x = () # empty Maybe
y = (3,) # Maybe with value 3
```

You can easily check whether an *Maybe* is empty:

```python
def f(x: int) -> Maybe[int]:
  return (x,) if x < 3 else ()

x: Maybe[int] = f(5)

if not x:
  print("Maybe is empty") # Maybe is empty
```

You can also provide an alternative value if *Maybe* is empty and immediately try to unwrap the *Maybe*:

```python
x: Maybe[int] = f(5)
y, *_ = x or (42,)

print(y) # 42
```

```python
# alternatively

x: Maybe[int] = f(1)
z = x or (42,)

# notice: if you pass an empty *z to a single argument function, you will get an error
print(*z) # 1
```

Because *Maybe* is simply a *tuple* under the hood, you can apply any Python function (that operates on *tuple*) to an instance of an *Maybe*.

### *as_catch*

*as_catch* is simply:

```python
@curry
def as_catch(default: Callable[[X], Y], xys: Iterable[Tuple[X, Y]]) -> Callable[[X], Y]:
  return catch(as_match(xys), default=default)
```

Example of *as_catch* usage:

```python
successor: Callable[[int], int] = Pipeline(range(10)) // zipmapr(lambda x: x + 1) >> as_catch(lambda _: -1)
print(successor(1)) # 2
print(successor(100)) # -1
```

### *as_either*

*as_either* is a function which allows you to create an *Either[Y, X]* from an *Maybe[X]*. *as_either* takes a function *Callable[[], Y]* and returns a function *Callable[[Maybe[X]], Either[Y, X]]*.

```python
raw_numbers = "1\n22\nten\n333".splitlines()

xs = (
  Pipeline(raw_numbers)
  / try_(int)
  / as_either(lambda: f"Failed to parse.")
  | print
)

# ((), (1,))
# ((), (22,))
# (('Failed to parse.',), ())
# ((), (333,))
```

The difference between using *as_either* and explicitly creating *Either* using tuples is that *as_either* will not evaluate the left part if the right part is present. That is why *Callable[[], Y]* is being passed to *as_either* instead of *Y*.

### *as_match*

*as_match* is simply:

```python
def as_match(xys: Iterable[Tuple[X, Y]]) -> Callable[[X], Maybe[Y]]:
  x_to_y = dict(xys)

  def lookup(x: X) -> Maybe[Y]:
    return (x_to_y[x],) if x in x_to_y else ()

  return lookup
```

Example of *as_match* usage:

```python
successor: Callable[[int], Maybe[int]] = Pipeline(range(10)) // zipmapr(lambda x: x + 1) >> as_match
print(successor(1)) # (2,)
print(successor(100)) # ()
```

### *between*

*between* is simply:

```python
def between(low: float, high: float) -> Callable[[float], bool]:
  return lambda x: low <= x and x <= high
```

Example of *between* usage:

```python
ys = filter(between(3, 5), range(10))
print(tuple(ys)) # (3, 4, 5)
```

### *both*

*both* is a function that takes a function *Callable[[X], Y]* and returns a function *Callable[[Tuple[X, X]], Tuple[Y, Y]]*. The returned function takes a pair and applies *Callable[[X], Y]* to both values.

```python
both(lambda x: x + 1)((1, 2)) # (2, 3)
```

### *cache*

*cache* is a decorator which returns a function that always returns a value that was returned in the first call.

```python
def f(x: int) -> int:
  return x + 5

g = cache(f)
print(g(5)) # 10
print(g()) # 10
print(g("abc", 1, {})) # 10

h = cache(f)
print(h(7)) # 12
```

### *catch*

*catch* is a function that resembles pattern-matching in Python. It takes some functions `*fs: Callable[..., Maybe[Y]]` with some catch-all function `default: Callable[..., Y]` and returns a function `Callable[..., Y]` which executes `fs` functions one by one until some function will return non-empty `Maybe[Y]`. If none of those functions will return a non-empty `Maybe[Y]`, the result of `default` function is returned.

```python
# let's say that we want to parse age ranges that we have in our data:
age_ranges = (
  "10-20",
  "20-30",
  "30+",
  "60+",
  "invalid input"
)

# we consider 30+ to be a valid range <30, 100)

def parse_range(x: str) -> Tuple[int, int]:
  raw = x.split("-")
  low, high, *_ = map(int, raw)

  return low, high

def parse_unbounded_range(x: str) -> Tuple[int, int]:
  raw, *_ = x.split("+")
  return int(raw), 100

# we will use <18, 100) as our default range
parse = catch(
  try_(parse_range),
  try_(parse_unbounded_range),
  default=lambda _: (18, 100)
)

for x in age_ranges:
  print(parse(x))

# (10, 20)
# (20, 30)
# (30, 100)
# (60, 100)
# (18, 100)
```

### *compose*

*compose* is an implementation of a ``Function composition" defined as $( f \circ g )(x) = f(g(x))$.

```python
xs = "a", "ab", "c"
yxs = enumerate(xs)

p: Callable[[Tuple[int, str]], bool] = compose(lambda x: x.startswith("a"), snd)
filtered: Iterable[Tuple[int, str]] = filter(p, yxs)

ys = map(fst, filtered)
print(tuple(ys)) # (0, 1)
```

### *curry*

*curry* is simply:

```python
def curry(f: Callable[..., Y]) -> Callable[..., Y]:
  return lambda *args, **kwargs: partial(f, *args, **kwargs)
```

### *drop*

*drop* is simply:

```python
def drop(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return (lambda xs: islice(xs, n, None)) if n > 0 else (lambda _: ())
```

Example of *drop* usage:

```python
xs = drop(1)(range(3))
print(tuple(xs)) # (1, 2)

xs = islice(range(3), 1, None)
print(tuple(xs)) # (1, 2)
```

### *except_*

*except_* is a decorator which returns a function that returns *Either* with some value or an *Exception* that was raised.

```python
f = except_(next)
xs = iter(range(2))

print(f(xs)) # ((), (0,))
print(f(xs)) # ((), (1,))
print(f(xs)) # ((StopIteration(),), ())
```

### *fail*

*fail* is a function which takes a function *Callable[[Exception], Y]* and returns a decorator which takes a function *Callable[..., Y]* and returns *Callable[..., Y]*. The function returned by the decorator uses passed *Callable[[Exception], Y]* to handle possible errors produced by a decorated function. If no errors produced, *Callable[[Exception], Y]* will not be executed and the result of the decorated function will be returned.

```python
# Let's say that you want to write is_repeated function
# which tells you whether you have a collection consisting
# only from the single value.

# The simplest function you could think of might look like this:

def is_repeated(xs: Iterable[X]) -> bool:
  x, *rest = xs
  return all(x == y for y in rest)

# It works on collections that have at least one value:

print(is_repeated((1, 1))) # True
print(is_repeated((1, 2, 3))) # False

# but when you have an empty collection, this function will result
# in an error:

print(is_repeated(()))
# ValueError: not enough values to unpack (expected at least 1, got 0)

# In order to handle this case, you can rewrite this function in a
# following manner:

def is_repeated(xs: Iterable[X]) -> bool:
  xs = iter(xs)
  wrapped_x = next_(xs)

  if wrapped_x:
    x, *_ = wrapped_x
    return all(x == y for y in xs)
  else: return True

# And it would work:

print(is_repeated((1, 1))) # True
print(is_repeated((1, 2, 3))) # False
print(is_repeated(())) # True

# You might also use a *fail* function which will surround your
# function with try-except clause, to deal with empty collection.

@fail(lambda _: True)
def is_repeated(xs: Iterable[X]) -> bool:
  x, *rest = xs
  return all(x == y for y in rest)

# In case when error is raised by is_repeated, the
# lambda _: True
# function will be executed. The raised error will be passed to
# that function.

def g(e: Exception) -> bool:
  print(e)
  return True

@fail(g)
def is_repeated(xs: Iterable[X]) -> bool:
  x, *rest = xs
  return all(x == y for y in rest)

print(is_repeated((1,))) # True
print(is_repeated(()))
# not enough values to unpack (expected at least 1, got 0)
# True
```

### *find*

*find* is a function which takes a predicate and returns a function which takes some *Iterable* and returns an *Maybe* with value that matches the predicate if such value exists:

```python
x: Maybe[int] = find(lambda x: x == 3)(range(5))
print(x) # (3,)

x: Maybe[int] = find(lambda x: x == -1)(range(5))
print(x) # ()
```

### *findindex*

*findindex* is a function that works like *find*, but instead of returning a function which returns a value in *Iterable* that matches some predicate, it returns a function which returns an index of that value in *Iterable*.

```python
x: Maybe[int] = findindex(lambda x: x == 8)(range(5, 10))
print(x) # (3,)

x: Maybe[int] = findindex(lambda x: x == -1)(range(5, 10))
print(x) # ()
```

### *finds*

*finds* is a function which takes an *Iterable[Callable[[X], bool]]* of predicates and returns a function which takes some *Iterable[X]* and returns an *Iterable[Maybe[X]]*. *finds* iterates over each predicate and searches for a matching value for that predicate in the passed *Iterable[X]*. *finds* will store checked *Iterable[X]* values in a buffer, so that the buffer will be checked at first and (if needed) the remaining *Iterable[X]* will be checked at last.

```python
fs = (lambda x: x == 2), (lambda x: x == 4), (lambda x: x == 1), (lambda x: x == -1)
ys: Iterable[Maybe[int]] = finds(fs)(range(5))

for y in ys:
  print(y)

# (2,)
# (4,)
# (1,)
# ()
```

### *flattenl*

*flattenl* is a function which takes a *Tuple* which contains another *Tuple* on the beginning and flattens that inner *Tuple* inside of outer *Tuple*.

```python
xys = {"A": 2.5, "B": 3.14}
Pipeline(xys.items()) // zipr(count(1)) / flattenl | print

# ('A', 2.5, 1)
# ('B', 3.14, 2)
```

### *flattenr*

*flattenr* is a function which takes a *Tuple* which contains another *Tuple* on the end and flattens that inner *Tuple* inside of outer *Tuple*.

```python
xys = {"A": 2.5, "B": 3.14}
Pipeline(xys.items()) // zipl(count(1)) / flattenr | print

# (1, 'A', 2.5)
# (2, 'B', 3.14)
```

### *flip*

*flip* is simply:

```python
def flip(f: Callable[[Y, X], Z]) -> Callable[[X, Y], Z]:
  return lambda x, y: f(y, x)
```

Example of *flip* usage:

```python
xs = "A", "B", "C"
Pipeline(enumerate(xs)) / key(lambda x: x + 1) * star(flip(repeat)) | print

# A
# B
# B
# C
# C
# C
```

### *foldl*

*foldl* is a function which takes a binary function *Callable[[Y, X], Y]* and some accumulator *Y* and returns a function which takes *Iterable[X]* and returns *Y*. This function allows you to fold *Iterable[X]* from __left__ using passed binary function. The accumulator is being passed as the __first__ argument of the binary function.

Example of *foldl* usage:

```python
xs = range(ord("A"), ord("Z") + 1)
alphabet = Pipeline(xs) / chr >> foldl(operator.add, "")

print(alphabet)

# ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

### *foldl1*

*foldl1* is a similar function to *foldl*. The difference between *foldl1* and *foldl* is that *foldl1* takes *Callable[[X, X], X]*, uses *Iterable[X]* __first__ element as the accumulator and returns *X*. *foldl1* will raise an error if the supplied *Iterable[X]* is empty.

### *foldr*

*foldr* is a function which takes a binary function *Callable[[X, Y], Y]* and some accumulator *Y* and returns a function which takes *Iterable[X]* and returns *Y*. This function allows you to fold *Iterable[X]* from __right__ using passed binary function. The accumulator is being passed as the __last__ argument of the binary function.

Example of *foldr* usage:

```python
xs = range(ord("A"), ord("Z") + 1)
reversed_alphabet = (
  Pipeline(xs)
  / chr
  // foldr(lambda x, acc: acc + [x], [])
  >> foldl(operator.add, "")
)

print(reversed_alphabet)

# ZYXWVUTSRQPONMLKJIHGFEDCBA
```

### *foldr1*

*foldr1* is a similar function to *foldr*. The difference between *foldr1* and *foldr* is that *foldr1* takes *Callable[[X, X], X]*, uses *Iterable[X]* __last__ element as the accumulator and returns *X*. *foldr1* will raise an error if the supplied *Iterable[X]* is empty. Under the hood *foldr1* will use *tuple* on passed *Iterable[X]* in order to extract the accumulator.

### *fst*

*fst* is simply:

```python
def fst(xy: Tuple[X, Y]) -> X:
  return xy[0]
```

### *group*

*group* is a function which takes *Iterable[X]* and returns *Iterable[Tuple[X, ...]]*. This function groups passed elements by equality comparison `==`.

```python
xs = 1, 1, 2, 2, 2, 3, 1, 1, 1
print(tuple(group(xs))) # ((1, 1), (2, 2, 2), (3,), (1, 1, 1))
```

### *groupby*

*groupby* is a function which takes an equality comparison function *Callable[[X, X], bool]* and returns a function *Callable[[Iterable[X]], Iterable[Tuple[X, ...]]]* which groups passed elements by the equality comparison function.

```python
people = (
  ("Alex", 23),
  ("John", 23),
  ("Sam", 27),
  ("Kate", 27),
  ("Fred", 23),
)

grouped = groupby(lambda x, y: snd(x) == snd(y))(people)
print(tuple(grouped))
# ((('Alex', 23), ('John', 23)), (('Sam', 27), ('Kate', 27)), (('Fred', 23),))

# or you can use *on* function:

grouped = groupby(on(operator.eq, snd))(people)
print(tuple(grouped))
# ((('Alex', 23), ('John', 23)), (('Sam', 27), ('Kate', 27)), (('Fred', 23),))
```

### *in_*

*in_* is simply:

```python
def in_(xs: Tuple[X, ...]) -> Callable[[X], bool]:
  return lambda x: x in xs
```

### *key*

*key* is simply:

```python
def key(f: Callable[[X], Z]) -> Callable[[Tuple[X, Y]], Tuple[Z, Y]]:
  g: Callable[[Tuple[X, Y]], Z] = compose(f, fst)
  return lambda xy: (g(xy), snd(xy))
```

Example of *key* usage:

```python
xys = {"A": [1, 2, 3], "B": [3, 4]}
zys = map(key(str.casefold), xys.items())

for zy in zys:
  print(zy)

# ('a', [1, 2, 3])
# ('b', [3, 4])
```

### *length*

*length* is a function which takes an *Iterable* and returns number of elements in that *Iterable*. *length* exhausts the *Iterable*.

```python
xs = 1, 2, 3
print(len(xs)) # 3

# len(iter(xs)) will raise an error
print(length(iter(xs))) # 3
```

### *lift*

*lift* is simply:

```python
lift = curry(map)
```

### *match_*

*match_* is a function that resembles pattern-matching in Python. It takes some functions `*fs: Callable[..., Maybe[Y]]` and returns a function `Callable[..., Maybe[Y]]` which executes `fs` functions one by one until some function will return non-empty `Maybe[Y]`. If none of those functions will return a non-empty `Maybe[Y]`, an empty `Maybe[Y]` (i.e. `()`) is returned.

```python
# let's say that we want to parse age ranges that we have in our data:
age_ranges = (
  "10-20",
  "20-30",
  "30+",
  "60+",
  "invalid input"
)

# we consider 30+ to be a valid range <30, 100)

def parse_range(x: str) -> Tuple[int, int]:
  raw = x.split("-")
  low, high, *_ = map(int, raw)

  return low, high

def parse_unbounded_range(x: str) -> Tuple[int, int]:
  raw, *_ = x.split("+")
  return int(raw), 100

parse = match_(
  try_(parse_range),
  try_(parse_unbounded_range)
)

for x in age_ranges:
  print(parse(x))

# ((10, 20),)
# ((20, 30),)
# ((30, 100),)
# ((60, 100),)
# ()
```

### *merge*

*merge* is a function which takes two sorted *Iterable[X]* and merges them into single sorted *Iterable[X]*. It uses *lambda x, y: x <= y* comparison function. Use *key* parameter to specify a function *Callable[[X], Y]* to be called on each element prior to making comparisons.

```python
xs = merge((1, 3, 5), (1, 2, 4))
print(tuple(xs)) # (1, 1, 2, 3, 4, 5)

xs, ys = [(1, "a"), (3, "d"), (5, "f")], [(1, "b"), (2, "c"), (4, "e")]
print(tuple((merge(xs, ys, key=fst))))
# ((1, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f'))
```

### *next_*

*next_* is simply:

```python
next_: Callable[[Iterator[X]], Maybe[X]] = try_(next)
```

Example of *next_* usage:

```python
xs = iter(range(2))

print(next_(xs)) # (0,)
print(next_(xs)) # (1,)
print(next_(xs)) # ()
```

### *not_*

*not_* is a function which takes a predicate and returns negation of that predicate.

```python
print(not_(lambda x, y: x == y)(1, 5)) # True
```

### *on*

*on* is simply:

```python
def on(f: Callable[[Y, Y], Z], g: Callable[[X], Y]) -> Callable[[X, X], Z]:
  return lambda p, n: f(g(p), g(n))
```

Example of *on* usage could be found in *groupby* section.

### *padl*

*padl* is a function which allows you to pad some *Iterable* from the __left__ using a filler. This function takes a number *n* and a filler *x*. In case when **exact=False** option is passed, it returns a function which prepends *n - k* fillers to the passed *Iterable*, where *k* is a length of the passed *Iterable*. In case when **exact=True** option is passed, it returns a function which prepends __exactly__ *n* fillers to the passed *Iterable*.

```python
xs = "".join(padl(5, "x")("abc"))
print(xs) # xxabc

xs = "".join(padl(5, "x", exact=True)("abc"))
print(xs) # xxxxxabc
```

### *padr*

*padr* is a function which allows you to pad some *Iterable* from the __right__ using a filler. This function takes a number *n* and a filler *x*. In case when **exact=False** option is passed, it returns a function which appends *n - k* fillers to the passed *Iterable*, where *k* is a length of the passed *Iterable*. In case when **exact=True** option is passed, it returns a function which appends __exactly__ *n* fillers to the passed *Iterable*.

```python
xs = "".join(padr(5, "x")("abc"))
print(xs) # abcxx

xs = "".join(padr(5, "x", exact=True)("abc"))
print(xs) # abcxxxxx
```

### *partition*

*partition* is a function which takes a predicate and returns a function *Callable[[Iterable[X]], Tuple[Tuple[X, ...], Tuple[X, ...]]]*. This returned function splits passed elements into those that do match the predicate and the rest. The difference between *span* and *partition* is that *span* stops when it finds the first element that does not match the predicate and *partition* goes until the end.

```python
xs = 1, 1, 2, 2, 2, 3, 1, 1, 1
matched, rest = partition(lambda x: x == 1)(xs)

print(matched) # (1, 1, 1, 1, 1)
print(rest) # (2, 2, 2, 3)
```

### *peek*

*peek* is a decorator which allows you to apply some function to a passed argument and return back the passed argument instead of a function's result.

```python
x = peek(print)(5) # 5
print(x) # 5

xs = (
  Pipeline(range(3, 0, -1))
  / peek(print, "Countdown:", file=sys.stderr)
  >> tuple
)
# Countdown: 3
# Countdown: 2
# Countdown: 1

print(xs) # (3, 2, 1)
```

### *pick*

*pick* is a function which takes some aggregate function *Callable[[Tuple[X, ...]], X]* and returns a function *Callable[[Iterable[X]], Iterable[X]]*. This returned function __picks__ all elements from the passed collection *Iterable[X]* which are equal to the value returned by the aggregate function. The equal function might be substituted with any other function of type signature *Callable[[X, X], bool]* by passing a *compare* parameter.

```python
print(min([1, 2, 1, 1, 3, 1])) # 1

ys = tuple(pick(min)([1, 2, 1, 1, 3, 1]))
print(ys) # (1, 1, 1, 1)

print(min([]))
# ValueError: min() arg is an empty sequence

ys = tuple(pick(min)([]))
print(ys) # ()
```

### *pickby*

*pickby* is a function which takes a function *Callable[[X], Y]*, an aggregate function *Callable[[Tuple[Y, ...]], Y]* and returns a function *Callable[[Iterable[X]], Iterable[X]]*. This returned function __picks__ all elements from the passed collection *Iterable[X]* which corresponding *Y* values, created by the *Callable[[X], Y]* function, are equal to the value returned by the aggregate function. The equal function might be substituted with any other function of type signature *Callable[[Y, Y], bool]* by passing a *compare* parameter. The function *Callable[[X], Y]* will be used exactly once on the whole collection.

```python
cars_and_prices = (
  ("Audi", 25000),
  ("BMW", 70000),
  ("Mercedes", 25000),
)

cheapest_car = min(cars_and_prices, key=snd)
print(cheapest_car) # ('Audi', 25000)

cheapest_cars = pickby(snd, min)(cars_and_prices)
print(tuple(cheapest_cars)) # (('Audi', 25000), ('Mercedes', 25000))
```

### *powerset*

*powerset* is a function which takes a *Tuple[X, ...]* and produces power set of those elements in form of *Iterable[Iterable[X]]*.

```python
xs = tuple(range(3))
ps = tuple(map(tuple, powerset(xs)))

print(ps) # ((), (2,), (1,), (1, 2), (0,), (0, 2), (0, 1), (0, 1, 2))
```

### *replicate*

*replicate* is a function which takes a number *n* and returns a function, which takes some value *x* and repeats *n* times value *x*.

```python
xs = tuple(replicate(5)("hello"))
print(xs)
# ('hello', 'hello', 'hello', 'hello', 'hello')
```

### *reverse*

*reverse* is a function which takes an *Iterable[X]* and returns *Deque[X]* which contains elements from *Iterable[X]* in reversed order.

```python
xs = range(ord("A"), ord("Z") + 1)

reversed_alphabet = (
  Pipeline(xs)
  / chr
  // reverse # Python reversed would not work on Iterable
  >> foldl(operator.add, "")
)

print(reversed_alphabet)

# ZYXWVUTSRQPONMLKJIHGFEDCBA
```

### *scanl*

*scanl* is a similar function to *foldl*. The difference between *scanl* and *foldl* is that *scanl* instead of returning a function which takes *Iterable[X]* and returns *Y*, returns a function which takes *Iterable[X]* and returns *Iterable[Y]*. The resulting *Iterable[Y]* contains all accumulators used in *foldl*.

```python
xs = scanl(operator.mul, 1)((1, 2, 3, 4, 5))
print(tuple(xs))
# (1, 1, 2, 6, 24, 120)
```

### *scanl1*

*scanl1* is a similar function to *foldl1*. The difference between *scanl1* and *foldl1* is that *scanl1* instead of returning a function which takes *Iterable[X]* and returns *X*, returns a function which takes *Iterable[X]* and returns *Iterable[X]*. The resulting *Iterable[X]* contains all accumulators used in *foldl1*.

```python
xs = scanl1(operator.mul)((1, 2, 3, 4, 5))
print(tuple(xs))
# (1, 2, 6, 24, 120)
```

### *scanr*

*scanr* is a similar function to *foldr*. The difference between *scanr* and *foldr* is that *scanr* instead of returning a function which takes *Iterable[X]* and returns *Y*, returns a function which takes *Iterable[X]* and returns *Deque[Y]*. The resulting *Deque[Y]* contains all accumulators used in *foldr*.

```python
xs = scanr(operator.mul, 1)((1, 2, 3, 4, 5))
print(xs)
# deque([120, 120, 60, 20, 5, 1])
```

### *scanr1*

*scanr1* is a similar function to *foldr1*. The difference between *scanr1* and *foldr1* is that *scanr1* instead of returning a function which takes *Iterable[X]* and returns *X*, returns a function which takes *Iterable[X]* and returns *Deque[X]*. The resulting *Deque[X]* contains all accumulators used in *foldr1*.

```python
xs = scanr1(operator.mul)((1, 2, 3, 4, 5))
print(xs)
# deque([120, 120, 60, 20, 5])
```

### *search*

*search* is a function which takes a predicate *Callable[[X], bool]* along with *Iterable[Y]* and returns a function which takes *Iterable[X]* and returns *Iterable[Y]*. This function zips *Iterable[Y]* with *Iterable[X]* and returns those *Y*s for which corresponding *X*s match the predicate.

```python
xs = search(lambda x: x > 3, count())(range(1, 6))
print(tuple(xs))
# (3, 4)
```

### *shift*

*shift* is a decorator which returns a partially applied function. The difference between Python's *functools.partial* and *shift* is that *shift* will return a function which prepends *\*args* and *\*\*kwargs*:

```python
def dummy(*args: object, **kwargs: object):
  print(args)
  print(kwargs)

partial(dummy, 1, 2, a=1, b="b")(3, 4, c="c")
print("-" * 10)
shift(dummy, 1, 2, a=1, b="b")(3, 4, c="c")

# (1, 2, 3, 4)
# {'a': 1, 'b': 'b', 'c': 'c'}
# ----------
# (3, 4, 1, 2)
# {'c': 'c', 'a': 1, 'b': 'b'}
```

Example of *shift* usage:

```python
take_3 = shift(islice, 3)
xs: Iterable[int] = take_3(range(5))

for x in xs:
  print(x)

# 0
# 1
# 2
```

### *slide*

*slide* is a function which takes a sliding window length **n** and a **step**, and returns a function which takes an *Iterable* and applies sliding window over it resulting in an *Iterable* of *tuple*s. Each *tuple* has at most length equal to **n**. In case when **exact=True** option is passed, each *tuple* has length equal to **n**. **step** is simply a shift of a sliding window.

```python
xs: Iterable[Tuple[int, ...]] = slide()(range(10))
print(tuple(xs))
# ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9,))

xs: Iterable[Tuple[int, ...]] = slide(n=3, step=2)(range(10))
print(tuple(xs))
# ((0, 1, 2), (2, 3, 4), (4, 5, 6), (6, 7, 8), (8, 9))

xs: Iterable[Tuple[int, ...]] = slide(n=3, step=2, exact=True)(range(10))
print(tuple(xs))
# ((0, 1, 2), (2, 3, 4), (4, 5, 6), (6, 7, 8))

def is_sorted(xs: Iterable[X], compare: Callable[[X, X], bool] = operator.le) -> bool:
  return (
    Pipeline(slide(exact=True)(xs))
    / star(compare)
    >> all
  )

print(is_sorted((1, 2, 5))) # True
print(is_sorted((1, 2, -5))) # False
```

### *snd*

*snd* is simply:

```python
def snd(xy: Tuple[X, Y]) -> Y:
  return xy[1]
```

### *span*

*span* is a function which takes a predicate and returns a function *Callable[[Iterable[X]], Tuple[Tuple[X, ...], Iterable[X]]]*. This returned function splits passed elements into those that do match the predicate on the beginning and the rest.

```python
xs = 1, 1, 2, 2, 2, 3, 1, 1, 1
matched, rest = span(lambda x: x == 1)(xs)

print(matched) # (1, 1)
print(tuple(rest)) # (2, 2, 2, 3, 1, 1, 1)
```

### *splitat*

*splitat* is a function which takes an index *i* and returns a function which splits an *Iterable[X]* into *Tuple[X, ...]* and *Iterable[X]*. The *Tuple[X, ...]* will contain first *i* elements and the *Iterable[X]* will contain the rest.

```python
xs, rest = splitat(1)(range(5))
print(xs) # (0,)
print(tuple(rest)) # (1, 2, 3, 4)
```

### *strip*

*strip* is a function which takes an *Iterable[X]* and returns an *Iterable[X]* with removed consecutive duplicates. *strip* functions uses only equality comparison `==`.

```python
xs = 1, 1, 2, 2, 2, 3, 1, 1, 1
print(tuple(strip(xs))) # (1, 2, 3, 1)
```

### *stripby*

*stripby* is a function which takes an equality comparison function *Callable[[X, X], bool]* and returns a function *Callable[[Iterable[X]], Iterable[X]]* which removes consecutive duplicates in terms of the equality comparison function.

```python
people = (
  ("Alex", 23),
  ("John", 23),
  ("Sam", 27),
  ("Kate", 27),
  ("Fred", 23),
)

stripped = stripby(lambda x, y: snd(x) == snd(y))(people)
print(tuple(stripped))
# (('Alex', 23), ('Sam', 27), ('Fred', 23))

# or you can use *on* function:

stripped = stripby(on(operator.eq, snd))(people)
print(tuple(stripped))
# (('Alex', 23), ('Sam', 27), ('Fred', 23))
```

### *take*

*take* is simply:

```python
def take(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return (lambda xs: islice(xs, n)) if n > 0 else (lambda _: ())
```

Example of *take* usage:

```python
xs = take(1)(range(3))
print(tuple(xs)) # (0,)

xs = islice(range(3), 1)
print(tuple(xs)) # (0,)
```

### *try_*

*try_* is a decorator which returns a function that returns *Maybe* with some value or an empty *Maybe* if an *Exception* was raised.

```python
load_json = try_(json.loads)

print(load_json("{}")) # ({},)
print(load_json("[1, 2, 3]")) # ([1, 2, 3],)
print(load_json("abc")) # ()
```

### *value*

*value* is simply:

```python
def value(f: Callable[[Y], Z]) -> Callable[[Tuple[X, Y]], Tuple[X, Z]]:
  g: Callable[[Tuple[X, Y]], Z] = compose(f, snd)
  return lambda xy: (fst(xy), g(xy))
```

Example of *value* usage:

```python
xys = {"A": [1, 2, 3], "B": [3, 4]}
xzs = map(value(len), xys.items())

for xz in xzs:
  print(xz)

# ('A', 3)
# ('B', 2)
```

### *where*

*where* is a similar function to *findindex*. The difference between *where* and *findindex* is that *where* returns indices of all elements that match given predicate instead of one. The other difference is that *where* returns a function which takes *Iterable[X]* and returns *Iterable[Y]*, on the other hand *findindex* returns a function which takes *Iterable[X]* and returns *Maybe[int]*.

```python
xs = where(lambda x: x >= 8)(range(5, 10))
print(tuple(xs)) # (3, 4)

xs = where(lambda x: x == -1)(range(5, 10))
print(tuple(xs)) # ()
```

### *zipflatl*

*zipflatl* is a function which takes a function *Callable[[X], Maybe[Y]]*, and returns some function which takes *Iterable[X]* and returns *Iterable[Tuple[X, Y]]* with only those elements from *Iterable[X]* that are mapped to non-empty *Maybe[Y]* by the function *Callable[[X], Maybe[Y]]*.

```python
xs = "1", "hello", "2"
f = try_(int)

ys = zipflatl(f)(xs)
print(tuple(ys)) # ((1, '1'), (2, '2'))
```

### *zipflatr*

*zipflatr* is a function which takes a function *Callable[[X], Maybe[Y]]*, and returns some function which takes *Iterable[X]* and returns *Iterable[Tuple[Y, X]]* with only those elements from *Iterable[X]* that are mapped to non-empty *Maybe[Y]* by the function *Callable[[X], Maybe[Y]]*.

```python
xs = "1", "hello", "2"
f = try_(int)

ys = zipflatr(f)(xs)
print(tuple(ys)) # (('1', 1), ('2', 2))
```

### *zipif*

*zipif* is a function which allows you to zip *Iterable[X]* elements with *Iterable[Y]* elements that match a predicate *Callable[[X, Y], bool]*, using a binary function *Callable[[X, Y], Z]*, into *Iterable[Z]*.

When a pair *x* and *y* do not match the predicate, a function *Callable[[X], Z]* is applied to *x* and its result is yielded. Also, in the next iteration only the first element *x* of the pair will be substituted with it's successor *x'* and *y* will remain unchanged (so that the predicate will get *x'* and *y*).

```python
participants = (
  ("Alex", 160.0),
  ("Sam", 0.0),
  ("Kate", 150.0),
  ("John", 155.0),
  ("Fred", 35.0)
)
name = fst
balance = snd

tickets = (
  (1, 160),
  (2, 150),
  (3, 300)
)
ticket_id = fst
price = snd

sell_tickets = zipif(
  lambda user, ticket: balance(user) >= price(ticket),
  lambda user, ticket: (name(user), balance(user) - price(ticket), (ticket,)),
  lambda user: (*user, ())
)

for x in sell_tickets(tickets)(participants):
  print(x)

# ('Alex', 0.0, ((1, 160),))
# ('Sam', 0.0, ())
# ('Kate', 0.0, ((2, 150),))
# ('John', 155.0, ())
# ('Fred', 35.0, ())
```

### *zipl*

*zipl* is simply:

```python
def zipl(xs: Iterable[X]) -> Callable[[Iterable[Y]], Iterable[Tuple[X, Y]]]:
  return lambda ys: zip(xs, ys)
```

Example of *zipl* usage:

```python
xs = "A", "B", "C"
Pipeline(xs) // zipl(count(1)) * star(flip(repeat)) | print

# A
# B
# B
# C
# C
# C
```

### *zipmapl*

*zipmapl* is simply:

```python
def zipmapl(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[Y, X]]]:
  return lambda xs: map(lambda x: (f(x), x), xs)
```

Example of *zipmapl* usage:

```python
xs = range(ord("a"), ord("z") + 1)
upper_to_lower = Pipeline(xs) / chr // zipmapl(str.upper) >> dict

Pipeline(upper_to_lower.items()) // take(5) | print

# ('A', 'a')
# ('B', 'b')
# ('C', 'c')
# ('D', 'd')
# ('E', 'e')
```

### *zipmapr*

*zipmapr* is simply:

```python
def zipmapr(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: map(lambda x: (x, f(x)), xs)
```

Example of *zipmapr* usage:

```python
xs = range(ord("a"), ord("z") + 1)
upper_to_lower = Pipeline(xs) / chr // zipmapr(str.upper) >> dict

Pipeline(upper_to_lower.items()) // take(5) | print

# ('a', 'A')
# ('b', 'B')
# ('c', 'C')
# ('d', 'D')
# ('e', 'E')
```

### *zipr*

*zipr* is simply:

```python
def zipr(ys: Iterable[Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: zip(xs, ys)
```

Example of *zipl* usage:

```python
xys = {"A": 2.5, "B": 3.14}
Pipeline(xys.items()) // zipr(count(1)) / flattenl | print

# ('A', 2.5, 1)
# ('B', 3.14, 2)
```
