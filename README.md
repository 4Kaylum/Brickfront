# Intro

Brickfront is a basic interface for working through Brickset's API. It should be pretty simple to use, though I do have the code reference if there's anyhing too difficult.

**Installation**:

```bash
pip install brickfront
```

# Getting Started

There's quite basic usage. For most things you don't need an API key, but for others `you may need to get one`__.

__ http://brickset.com/tools/webservices/requestkey

First you need to make a `Client` object.

```python
>>> import brickfront
>>> client = brickfront.Client(API_KEY)
```

From there, you can make requests through your client to be able to get different sets.

```python
>>> setList = client.getSets(query='star wars')
>>> len(setList)
20
>>> build = setList[18]
>>> build.name
"Jabba's Palace"
>>> build.pieces
'231'
>>> build.priceUK
'27.99'
```

Most code is fully internally documented, so it will autofill and properly interface with Python's `help` function.

API Reference
--------------------

[Click here](https://brickfront.readthedocs.io/en/latest/index.html)
