# YC Secret

Library for interaction with the Yandex Cloud Lockbox service

## Installing YC Secret

YC Secret is available on PyPI:

```
$ python -m pip install yc-secret
```

YC Secret officially supports Python 3.7+.

Key Features
============

- Unlimited number of secret ids (limited by system only)
- Getting the list of keys by secrete ids
- Getting particular key without using a secret id

Getting started
===============

You need to define all secret ids in one line and put it into environment You also need to use ``YCSECRET`` as variable
Please note that symbol ``|`` is being used as separator

Code example
------

How to get the content of the secret

```python
secret = Secret(token)
secret_value = secret.get_secret("yg854tgreg9ger")
```

How to get the content of the key

```python
secret = Secret(token)
key_value = secret.get_key("yg854tgreg9ger")
```

Requirements
============

- Python >= 3.7
- aiohttp

License
=======

``YC Secret`` is offered under the Apache 2 license.