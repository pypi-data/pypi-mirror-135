# Suppres

Decorator to ignore exceptions in functions. A simple wrapper around contextlib.suppress.

## Install

```
pip install suppress
```

## Usage

```python
from suppress import suppress


@suppress(ZeroDivisionError)
def zero_error_function():
    1/0


def main():
    print('First print')
    zero_error_function()
    print('Second print')


if __name__ == '__main__':
    main()
```
Output:

```
First print
Second print
```
