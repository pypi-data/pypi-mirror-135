# config_manager
Configuration manger

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
test_config_age=33 python example_parser.py --name hello
```

It will output something like and all the *primitive* types will be parsed correctly:

```
age = 33
is_useful = True
name = hello
```
