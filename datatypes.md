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

In my project, strings are only used for label displays on text, applications and buttons, as well as for keys in dictionaries.

## Integer
An integer (`int` in python) stores whole numbers; they cannot contain any decimals. Unlike other programming languages such as C++ where integers have limited precision, which defines how many digits can be stored in a variable of certain type, dictated by the underlying binary, python's integers have unlimited precision (as of python 3). This means that integers can be arbitrarily large, without the need for type qualifiers such as `long`. Integers can be positive or negative.

Integers can 