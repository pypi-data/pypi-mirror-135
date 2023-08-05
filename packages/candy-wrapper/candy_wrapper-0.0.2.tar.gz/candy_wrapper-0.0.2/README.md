# Candy Wrapper
Candy Wrapper is a "sticky" wrapper for any object, which adds syntax surgar.

## Usage

```python
from candy.candy_wrapper import Wrapper
foo = SomeClass()
candy = Wrapper(foo)
foo['bar'] = 42
print(foo.bar) # prints 42
setattr(foo,'hey',420)
print(foo['hey']) # prints 420
```
