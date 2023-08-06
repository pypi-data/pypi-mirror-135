# glibs

[![CI](https://github.com/projetoeureka/glibs/actions/workflows/ci.yml/badge.svg)](https://github.com/projetoeureka/glibs/actions/workflows/ci.yml)

Collection of utilties (and a namespace package for other packages) to use in our Python projects

## What's included?

### `glibs.utils`

#### `dictutils`

- `CaseInsensitiveDict`

  A `dict` that is case-insensitive for setting and accessing items:

  ```python
  items = CaseInsensitiveDict()
  items["Key"] = "value"
  items["key"]  # -> "value"
  ```

#### `funcutils`

- `retry(f, exceptions, max_tries, delay, logger)`

  Calls `f()` and retry automatically if it raises an exception.

    * `exceptions`: if `f()` raises an exception that is not listed here, that exception will bubble (making the function to not be retried). Accepts one or a tuple of exception classes. Default is `Exception`

    * `max_tries`: the max number of times `f()` will be executed. `1` means it won't retry, `2` means it will retry once. Default is `-1` which is equivalent as infinite.

    * `delay`: how many seconds to wait between tries. Accepts a number (fixed wait time between tries) or a generator. Default is `iterutils.exponential(2)`.

- `with_retry(exception, max_tries, delay, logger)`

  A decorator that will make the decorated function retry automatically if it raises an exception. Same arguments as `retry`.

#### `stringutils`

- `remove_accents(text)`

#### `timeutils`

- `to_isoformat(datetime)`

  Returns a `datetime` string formatted as ISO-8601 with the Z flag automatically.

- `from_isoformat(string)`

  Parse a ISO-8601 string and returns a `datetime`.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).
