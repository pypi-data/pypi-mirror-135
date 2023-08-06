# fastack-mongoengine

[MongoEngine](https://github.com/MongoEngine/mongoengine) integration for [fastack](https://github.com/fastack-dev/fastack).

# Installation

```
pip install fastack-mongoengine
```

# Usage

Add the plugin to your project configuration:

```python
PLUGINS = [
    'fastack_mongoengine',
    ...
]
```

Configuration:

* ``MONGODB_URI``: MongoDB URI.
