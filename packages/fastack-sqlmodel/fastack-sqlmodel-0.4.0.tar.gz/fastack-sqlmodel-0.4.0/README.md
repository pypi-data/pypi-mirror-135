# fastack-sqlmodel

[SQLModel](https://github.com/tiangolo/sqlmodel) integration for [fastack](https://github.com/fastack-dev/fastack).

# Installation

```
$ pip install fastack-sqlmodel
```

# Usage

Add the plugin to your project configuration:

```python
PLUGINS = [
    'fastack_sqlmodel',
    ...
]
```

Configuration:

* ``SQLALCHEMY_DATABASE_URI``: The database URI.
* ``SQLALCHEMY_OPTIONS``: Additional parameters for the SQLAlchemy engine.
