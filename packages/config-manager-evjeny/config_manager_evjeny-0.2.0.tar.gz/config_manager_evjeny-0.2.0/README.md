# config_manager
Configuration manager for parsing from different sources

## Installation

```bash
python -m pip install config-manager-evjeny
```

## Usage

Create class with config variables and inherit it from `config_manager.config.Config`.
You can define variables and their types or even define values.
Then we can parse variables from different sources.
For example, this is [example_parser.py](example_parser.py):

```python
from config_manager import config


class TestConfig(config.Config):
    name: str
    age: int
    is_useful: bool = False


my_config = TestConfig()
config.parse_env(my_config, prefix="test_config_")
config.parse_json(my_config, json_path="test_config.json")
config.parse_arguments(my_config, "TestConfig parser")

print(my_config)
```

If we run it:

```bash
test_config_age=33 python example_parser.py \
  --name hello \
  --is_useful false \
  --parts 0.25 0.5 0.75
```

It will output something like and all the *primitive* types will be parsed correctly:

```
age = 33
is_useful = False
name = hello
parts = [0.25, 0.5, 0.75]
```

## Type details

### `str`, `int` and `float`

For `str`, `int` and `float` casting is the same as builtin functions.

### `BoolType`

Generally all not empty containers (even string `"false"`)
cast to `bool` would return `True`.

Thus, there is custom type `BoolType`.
Variable cast to `BoolType` will get `True` value in one of these cases:
* variable is subclass of `str` and it's value one of (in any case):
  * `"yes"`
  * `"true"`
  * `"1"`
  * `"on"`
* variable is numeric, and it's value is `1` (or `1.0`)

```python
from config_manager.config_types import BoolType

assert BoolType("yes") == True
assert BoolType("yES") == True
assert BoolType("tRuE") == True
assert BoolType("1") == True
assert BoolType("on") == True

assert BoolType("no") == False
assert BoolType("FaLsE") == False

assert BoolType(1.0) == True
assert BoolType(0.0) == False
assert BoolType(1) == True
assert BoolType(0) == False
assert BoolType(True) == True
assert BoolType(False) == False
```

### `ListType`

As it is impossible to get type from `typing.List[T]`
(plus this annotation removed in Python 3.9) there is a `ListType`.
It can be used with any of primitives, so every element will be cast
to primitive's type. For example:

```python
from config_manager.config_types import ListType

assert ListType[int](["1", "2", "3"]) == [1, 2, 3]
assert ListType[str]([1.0, -213.5122, 52.123]) == ["1.0", "-213.5122", "52.123"]
```

All the parse sources provide different ways to define list, so there they are:
* in `predefine` and `json` case simply assign any python list to variable
* in `environment` case provide list separated by comma without spaces, like `my_cool_list=hello,world,ough`
* in `argument` case put list items separated by spaces after variable name, like `--cool_list 1 2 3 1123`
