*What is a datatype?*

In programming, a datatype is a classification used to determine what type of data a given variable can store. The type of data influences how the variable can be manipulated, including what methods (operations) can be performed. Different datatypes have different purposes, hence why there is no "one" universal datatype. In theory, a universal datatype could be possible, but would be infeasible due to performance optimizations when working with specific types of data. 

Python has several builtin datatypes, including but not limited to;
- int (integer)
    - `1, 2, -100`
- float (floating point number)
    - `1.0, 2.0, -100.995, float('inf')`
- complex (complex numbers, with j referencing the imaginary unit)
    - `1 + 2j`
- str (string)
    - `"foobarbaz"`
- list (collection of variables, mutable *(entities can be modified after creation)*)
    - `[1, 2, 3], ['foo', 'bar', 'baz']`
- tuple (collection of variables, immutable *(entities cannot be modified after creation)*)
    - `(1, 2, 3), ('foo', 'bar', 'baz')`
- dict (dictionary)
    - `{'foo': 'bar', 'baz': 1}`
- bool (boolean)
    - `True or False, 1 or 0`
- NoneType (None)

## Bool
A boolean value is the most fundamental datatype in programming, analogous across all programming languages; it is always either True or False, 1 or 0. It is the lowest abstraction in computing, where electrical impulses of high or low determine complex flow within a physical chip. All other datatypes can be said to be a collection of boolean values, or binary. For the purposes of this, and in the case of python, bool is simply used to store a binary True or False. The primary use case for boolean values is in logic control. For example, a simple if statement evaluates an expression and diverts the flow logic based on the boolean outcome:

```python
if var_a < var_b:
    print("var_a is less than var_b")
else:
    print("var_a is greater than var_b")
```

The if statement evaluates `var_a < var_b` using the relational operator `<`. The operator returns `True` if `var_a` is less than `var_b`, and `False` if the contrary is true. The if statement then proceeds with the code indented under the statement if that statement evaluated to `True`, and would proceed to the `else:` block if not.

Boolean values can be assigned to as variables. The previous example could be written as:

```python
result = var_a < var_b
if result:
    print("var_a is less than var_b")
else:
    print("var_a is greater than var_b")
```

And would yield the same results.

Binary operations can be performed on boolean values in python:

```python
a = True
b = False
c = True

print(a and b) # False (AND)
print(a or b) # True (OR)
print(not a) # False (NOT)
print(a ^ b) # True (XOR)
print(a ^ c) # False (XOR)
```

- `AND` returns `True` if both variables are `True`, otherwise `False`
- `OR` returns `True` if either variable is `True`
- `NOT` negates the value of a variable, returning its inverse
- `XOR` or *Exclusive OR*, returns `True` if **exactly one** variable is `True`, and `False` is both are the same

The methods of many other datatypes will return boolean values, for example a string's `.isalpha()` will return `True` if the string is alphanumeric, and `False` otherwise. Hence, and even outside of the low level binary usage of boolean, it is clear how universal the datatype `bool` is in python.

My code uses boolean values extensively, primarily for flow and logic control, but also for binary parameter storing; such as through buttons.

## String
A string (`str` in python) is a sequence of characters. Unlike other programming languages such as C++, where strings are basically a list of characters, any given character is a string. Technically, a string is a single character, and hence the datatype is a string of strings, because a string can be indexed and sliced. Strings are commonly used for storing user input, and storing information to be displayed.

While strings can be modified using operators such as +, they are *immutable*, meaning their value cannot be changed after creation. Hence, an operator such as `+=`, which could be percieved as directly modifying the string, actually creates a temporary buffer that stores the old string, and the new value, then writes the buffer to back to the string. Because of this, using strings for any mathematical calculations or performant scenarios is not good practice.

However, the primary use case for strings (in python), is most likely user input and output. A string in python can represent any Unicode character, including emojis, letters, numbers and other special characters. This makes them a safe datatype for handling arbitrary user input without validation, or with delayed validation.

```python
var = string(input("Enter text: "))
foo = "foo"
bar = "bar"

print(foo + bar) # foobar
print(foo * 2) # foofoo
print(foo[0]) # f
print((foo+bar)[-1]) # r
```

In my project, strings are only used for label displays on text, applications and buttons, as well as for keys in dictionaries.

## Integer
An integer (`int` in python) stores whole numbers; they cannot contain any decimals. Unlike other programming languages such as C++ where integers have limited precision, which defines how many digits can be stored in a variable of certain type, dictated by the underlying binary, python's integers have unlimited precision (as of python 3). This means that integers can be arbitrarily large, without the need for type qualifiers such as `long`. Integers can be positive or negative.

Integers can be operated on mathematically, using all of the most common methods and operators:

```python
a = 1
b = 2

print(a+b) # 3
print(a-b) # -1
print(a*b) # 2
print(int(a/b)) # 0 (rounds back down)
print(a**b) # 1
# and so forth
```

Notice the statement where `int()` is called on the resultant of `a/b`. When we divide `a` and `b`, we get a floating point number. In the print expression, we assign it back to an integer using the function call `int()`. This will round it down to a whole number. It will never round up.

```python
print(int(0.9)) # 0
```

Integers can be used in complex mathematical calculations, but because of this limitation with rounding, you would never explicitly cast a floating point resultant back into an integer. Instead, the `round()` function should be used, where accuracy can be specified.

Python is *dynamically typed*, which in short means that variables cannot be explicitly assigned to a datatype; instead, they can change after declaration. Because of this, integers cannot be "relied" on as as a datatype for calculations, especially when dealing with arbitrary data, as python will in most cases convert it to a floating point at the end of an expression. In other languages such as C++, which is statically typed, you cannot assign floating point values to integers, allowing much more declarative and rigid code.

Hence, in my project, integers are primarily used as indexes into arrays, or for window coordinates that cannot be fractional. Compound datatypes (arrays, lists etc), as will be later explained, can return values given an index. These indices are *almost* always whole numbers.

_\*in a dunder \_\_iter\_\_ method for a custom class, you could define whatever datatype you want to, in order to index a value from a list_

## Floating point
A floating point number shares all of the same properties as integers, including most of the same methods and functions. The primary difference in python is that floating point numbers can have arbitrary decimal precision. Floating point numbers, like integers, have unlimited precision.

```python
a = 0.1
b = 0.5
infinity = float('inf')

print(a+b) # 0.6
print(infinity) # inf
print(infinity/2) # inf
print(infinity*0) # nan
```

Notice the `float('inf')` casting. This is a special datatype that has infinite value. It is very useful for calculating the lowest value, as nothing can be higher than it. It is used in my code to calculate a lowest value:

```python
penetration = float('inf')

# ...
for value in something:
    offset = some_calculation

    if offset < penetration:
        penetration = offset
    # ...
```

I assign penetration infinity, and then traverse through a list to determine the lowest value for offset that is less than penetration. This could be achieved by setting penetration to an arbitrarily high number, like `99999`, but this does not account for a scenario where offset is initially potentially higher.

Otherwise, floating points are used very frequently through my code, to store everything from gravity constants to restitution to delta times to times in nanoseconds.


## Lists
A list, or vector in C++, is a datatype that can store any other datatypes. It is a "container", where any element inside the list can be retrieved and indexed by its offset from the beginning. As touched on previously, a string is technically a list, as you can index any character in a string with its index, and preform most of the list operations on it. In python, list indices begin at 0 and continue for each entry in a list. It is created using square brackets.

```python
foo = ["b", "a", "r"]
print(foo[0]) # b
print(foo[1]) # a
print(foo[-2]) # a
print(foo[0:-1]) # a
```

A list item can be retrieved front to back using negative indices. It can also be "sliced" with `:`, which returns elements in a range. 

New variables can be assigned to existing values:

```python
foo = ["b", "a", "r"]
print(foo[0]) # b
foo[b] = "c"

print(foo[0]) # c
```
Elements can also be appended with the method `list.append()`, and removed with `list.pop(index)`. Popping an element out of the list will return it back.

Lists are very useful when order matters and you need to return something by its index. Iteration through elements is simple, and the order will stay the same. However, removing elements from a position in the list can be impactful on performance, as python has to iterate through the entire list in order to move other elements down.

Lists are used frequently throughout my application, for storing sequential vertices in a shape, bodies in an engine and more, where repeatable, sequential and indexable access is required.

## Tuple
A tuple is similar to a list in the sense that data can be retrieved by its index. However, tuples are immutable, so elements cannot be removed or added after creation. This is the main difference between the two.

Their immutability has a few benefits over lists. Because their size is set at declaration, searching through elements by index is faster with lists, especially with an increase in items. They can also be used for dictionary keys, which will be explained later.

```python
foo = ("a", "b", "c")
print(foo[0]) # a
print("b" in foo) # True
foo.pop(0) # error
```
Tuples are not used in my application, as all lists need to be dynamically allocated and modified due to the "updating" nature of a physics engine. There is one case where a tuple could be used inside a custom class, and in one instance it would improve performance, but to re-use code a list will suffice.

## Dictionary
A dictionary, or `dict` in python, is an ordered list where each item is indexed by a unique value, known as a key-value pair. Only immutable values can be used for keys, which means that lists and other dictionaries cannot be used in the key field.

```python
foo = {"big": True, "bar": "yes"}
print(foo["big"]) # True
```

In the above example we return the value given a key. We cannot index an item in a dictionary given an index, unless the key is numerical, unless we iterate over all elements:

```python
foo = {"big": True, "bar": "yes"}
counter = 0
target = 1
for key, value in foo:
    if counter == target:
        print(key, value)
        break
    counter += 1
```

For obvious reasons, this is not very performant. However, it is not an issue when you consider the types of data that is commonly stored in a dictionary; properties, pairings and more.

A common use case for a dictionary, and one that is used in my application, is storing a list of dictionaries:
```python
some_list = []

for i in range(10):
    some_list.append({"index": i, "value": f"foobar+{i}")

print(next(item['value'] for item in some_list if item['index'] == 1)) # foobar1
```

## Custom
Custom datatypes are very powerful. They allow you to aggregate multiple other datatypes and control which methods do what with the data, making using them highly declarative. This can be accomplished in python using the `class` keyword, and similarly in other programming languages.

```python
class Dog:
    def __init__(self, name, breed, weight, age):
        self.name = name
        self.breed = breed
        self.weight = weight
        self.age = age

    def get_age(self, dog=False):
        if not dog:
            return self.age
        if self.age <= 2:
            dog_years = self.age * 10.5
        else:
            dog_years = 21 + (self.age - 2) * 4
        return dog_years

dog_1 = Dog("otis", "German Shorthaired Pointer", 35, 2.5)
print(dog_1.name) # otis
print(dog_1.get_age(dog=True)) # 23.0
print(class(dog1)) # <class '__main__.Dog'>
```

This is a simple example of a custom datatype. We can set parameters in the dunder `__init__` (double underscore), which is a *magic method*, being a constructor. We can then define other arbitrary methods for manipulating, validating or returning our data.

```python
type Scalar = int | float
class Vec2:
    def __init__(self, x: Scalar = 0.0, y: Scalar = 0.0):
        self._x: Scalar = x
        self._y: Scalar = y

    #...

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self._x + other.x, self._y + other.y)
```

The above code is a more complicated example, and an excerpt from my program. It is intended to store vectors, which is an object that contains magnitude and direction. This is generalised to improve re-usability.

We can annotate types using `varname: type = variable`, which informs python's type checker what datatype should be stored in a variable, and can help with lsp errors. It also improves the readability of code by defining what a variable might be, or what a function might return.

A custom type can be defined using the `type` keyword, which is builtin as of python version 3.12. Here, we define a `Scalar`, which is a single numerical value; having only magnitude and no direction. We can specify that we want either an integer or a floating point number using the union type (`|`).

Notice the `__add__` method. This is another magic method, and it instructs python on how to handle addition with a custom class. Here, we allow addition by summing the respective `x` and `y` properties of the new value, and return it.

This would allow us to do the equivalent of:

```python
a = Vec2(1, 2)
b = Vec2(1, 3)

c = a+b

print(c.x, c.y) # 2, 5
```

While this is a basic example, my code extends this greatly to allow various complicated vector operations, which greatly simplifies code and improves legibility over disjointed functions.

As is probably obvious, custom datatypes are crucial to my code, but not absolutely critical. We could have used a list for `a` and `b`, but this is less readable, declarative and clean. Hence, they are used widely throughout, where builtin types won't suffice.

## Date and time
Date and time could store a date in a given format based on locality. However, python does not have a built in date or time datatype, rather it is provided by the python module datetime.

```python
from datetime import datetime, timedelta
dt = datetime(2008, 11, 15, 12, 30)

print(dt) # 2008-11-15 12:30:00
print(dt + timedelta(days=16 * 365)) # 2024-11-11 12:30:00
```

This allows for operations given dates and times, and would be useful for time-based records or timewise operations. In my application, I do not use the datetime module.

Instead, I do use time based operations, but they are stored as floating point numbers; representing milliseconds and nanoseconds.

```python
import time
time_ = time.perf_counter_ns()
# some execution logic
print(time_)  # 138851434332218

```

This function of the time module will return a nanosecond timestamp using the underlying operating systems best and most accurate clock. It measures millisecond offset from the start of program execution, which means it will never go backwards. Hence, it is very useful for calculating precise measurements of time. I use it in my program to determine how far a mouse cursor has moved over a given point in time to determine velocity ($v = d/t$). However, it is not actually a datatype, and uses integers for storage.


## Real
A real number is any number that can be placed on an infinite number line. It includes rational and irrational numbers, where rational numbers can be expressed as fractions and irrationals can't. It can be either negative or positive, with infinite precision. It encompasses all numbers besides irrational, complex and special numbers such as infinity.

It is very useful as a broad "valid number" datatype. In python, Real is not considered a datatype on its. Own. However, it can be created as a type definition for simplicity sake. Type annotation in short tells python what datatype is expected of a function return or variable. It is not a requirement.

```python
type Real = int | float

somenumber: Real = 0.9999
somenumber += j # still works
```

However, if ensuring that **only** real numbers is stored within a variable, a custom Real class could be created:

```python
class Real:
    def __init__(self, value: float):
        self.value = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float):
        if not isinstance(new_value, (int, float)):
            raise ValueError("Value must be a real number (int or float).")
        self._value = float(new_value)
```

Here we define a property and a setter using a method and a decorator. By creating a method with the same name as a property, we can control exactly what can and can't be assigned to the variable. We define two methods, as python supports overloading of functions, so calling `var.value` will be different to `var.value = foo` and will call the relevant functions. This is furthered by the decorators specified by `@`, which informs language servers (extensions) that the property is defined by the setter and the property. It can then enforce the logic found in the if statement within the setter, which ensures that the new set value will be either an integer or a float.

## Array
An array is analogous to a list.

## Record
A record is a collection of related information. A product may contain related information about origin, price, nature etc. In python, there is no "Record" per-se, however the closest datatype would be a dictionary which is defined above. A named tuple can also be used to explicitly define properties for a tuple:

```python
from collections import namedtuple

Student = namedtuple('Student', ['name', 'age', 'DOB'])

S = Student('Arthur', '16', 2008)

print(s.name) # Arthur
```

This could also be achieved with a custom class.

A record is very useful for storing related data and retrieving it later. In the above example, student records could be stored in a list, and individual fields can be returned. In my program, I don't explicitly use records or named tuples in my application, but the concept of a record is used to store rigid body properties.

## Trees
A tree is a hierarchical abstract datatype that consists of nodes (vertices) connected by edges. It can be considered a "tree" because it contains leaves and branches. Each node can be connected to other nodes and form a branch-like structure.
```
        Root
       /    \
   Child 1   Child 2
   /    \
Child 1.1 Child 1.2
```

The topmost node is known as the root, and the bottom nodes with no children are considered "leaves". Because of the hierarchical structure of trees, they are excellent for representing relationships between data. For example, a filesystem directory structure could be stored as a tree, which would allow traversal and calculation of "depth" based on the number of node relationships. Trees and tree-based algorithms are prevalent in many builtin python functions, including the dictionary datatype which is actually stored like a tree. However, there is no user-facing tree datatype. Instead, it could be created using node and tree classes:

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class Tree:
    def __init__(self, root_value):
        self.root = TreeNode(root_value)
    # ...
```

I do not explicitly use trees in my application, with the exception of dictionaries, as the nature of my application does not lend itself to it.

## Sequential and random files
Sequential files refer to files that are accessed sequentially (linearly), which means that data is written or read in a specific order, generally from top to bottom. They contrast with random access files, which allow seeking to any point in the file without reading the previous lines. Sequential file operations are typically preferred for larger files, as reading and writing can be optimized in single streams; reducing the need for seeking to different spots in the file. However, for random access, as the name implies, random access files are more performant than sequential files, but they do have added overhead. This is the premise of sequential access memory (sam), but physical media using sam is more uncommon and typically limited to specific cases such as magnetic tape drives, where data can only be accessed linearly. Modern storage media almost exclusively uses random access memory, and so does computer memory.

In python, files can be read either sequentially or randomly using the builtin `open` function, but sequential access is much more common:

```python
with open('foobar.txt' 'w') as file:
    for line in file:
        print(line, end="")

    file.write("baz")
```

Using the `with` keyword when calling open is best practice as python will handle closing the file when all operations are complete. This is important, as in the name of optimization, python may not always write changes to files immediately, instead waiting for a buffer to fill up and writing out the entire buffer to the file.

We can also write content to a file. Again, once execution within the `with` statement finishes python will close the file. This is the same as calling `file.close()`.

I use sequential files in my application to read in lesson content from markdown files, however it is readonly, and uses the `.read()` method on the file to assign its contents to a variable.
