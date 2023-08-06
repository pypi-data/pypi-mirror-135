# flypper-redis

Flypper-redis is a storage backend for the [flypper](https://github.com/nicoolas25/flypper) package.

It is backed by Redis so it an be used in a distributed environment and be persisted across restarts.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `flypper-redis`.

```bash
pip install flypper-redis
```

## Usage

Build a storage backend:

```python
from redis import Redis
from flypper_redis.storage.redis import RedisStorage

redis = Redis(host="localhost", port=6379, db=0)
storage = RedisStorage(redis=redis, prefix="flypper-demo")
```

Use it in the web UI:

```python
from flypper.wsgi.web_ui import FlypperWebUI

web_ui = FlypperWebUI(storage=storage)
```

Use it in your code:
1. Build a client for your app
2. Use a context

```python
from flypper.client import Client as FlypperClient

# Once per thread
flypper_client = FlypperClient(storage=storage, ttl=10)

# Once per request
flypper_context = FlypperContext(
    client=flypper_client,
    entries={"user_id": "42"},
)

# Every time you need
flypper_context.is_enabled("flag_name")
flypper_context.is_enabled(
    "other_flag_name",
    entries={"item_reference": "blue-shampoo"},
)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
