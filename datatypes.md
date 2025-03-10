*What is a datatype?*

In programming, a datatype is a classification used to determine what type of data a given variable can store. The type of data influences how the variable can be manipulated, including what methods (operations) can be performed. Different datatypes have different purposes, hence why there is no "one" universal datatype. In theory, a universal datatype could be possible, but would be infeasable due to performance optimizations when working with specific types of data. 

Python has several builtin datatypes, including but not limited to;
- int (integer)
    - `1, 2, -100`
- float (floting point number)
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

The if statement evalates `var_a < var_b` using the relational operator `<`. The operator returns `True` if `var_a` is less than `var_b`, and `False` if the contrary is true. The if statement then proceeds with the code indented under the statement if that statement evaluated to `True`, and would proceed to the `else:` block if not.

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

However, the primary use case for strings (in python), is most likely user input and output. A string in python can represent any Unicode character, including emojis, letters, numbers and other special characters. This makes them a safe datatype for handeling arbitrary user input without validation, or with delayed validation.

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

\**in a dunder \__iter__ method for a custom class, you could define whatever datatype you want to, in order to index a value from a list*

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