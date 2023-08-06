# simplestr
A python package with annotations to automatically generate `__str__(self)`, `__repr__(self)` and `__eq__(self, other)` methods in classes


# Description
This package provides only two annotations:
- `@gen_str` to generate `__str__(self)` method
- `@gen_repr` to generate `__repr__(self)` method
- `@gen_eq` to generate `__eq__(self, other)` method 
- `@gen_str_repr` to generate both `__str__(self)` and `__repr__(self)` methods
- `@gen_str_repr_eq` to generate both `__str__(self)`, `__repr__(self)` and `__eq__(self, other)` methods

# Installation
 
## Normal installation

```bash
pip install simplestr
```

## Development installation

```bash
git clone https://github.com/jpleorx/simplestr.git
cd simplestr
pip install --editable .
```

# Example A (with separate annotations)
```python
from simplestr import gen_str, gen_repr, gen_eq

@gen_str
@gen_repr
@gen_eq
class Rect:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

rect1 = Rect(1, 2, 3, 4)
rect2 = Rect(10, 20, 30, 40)
print(rect1)
print(rect2)
print([rect1, rect2])
print(rect1 == rect2)
print(rect1 == Rect(1, 2, 3, 4))
```

```
Rect{x=1, y=2, w=3, h=4}
Rect{x=10, y=20, w=30, h=40}
[Rect{x=1, y=2, w=3, h=4}, Rect{x=10, y=20, w=30, h=40}]
False
True
```

# Example B (with joined annotation)
```python
from simplestr import gen_str_repr_eq

@gen_str_repr_eq
class Rect:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

rect1 = Rect(1, 2, 3, 4)
rect2 = Rect(10, 20, 30, 40)
print(rect1)
print(rect2)
print([rect1, rect2])
print(rect1 == rect2)
print(rect1 == Rect(1, 2, 3, 4))
```

```
Rect{x=1, y=2, w=3, h=4}
Rect{x=10, y=20, w=30, h=40}
[Rect{x=1, y=2, w=3, h=4}, Rect{x=10, y=20, w=30, h=40}]
False
True
```

# Links
In case you’d like to check my other work or contact me:
* [Personal website](https://tekleo.net/)
* [GitHub](https://github.com/jpleorx)
* [PyPI](https://pypi.org/user/JPLeoRX/)
* [DockerHub](https://hub.docker.com/u/jpleorx)
* [Articles on Medium](https://medium.com/@leo.ertuna)
* [LinkedIn (feel free to connect)](https://www.linkedin.com/in/leo-ertuna-14b539187/)