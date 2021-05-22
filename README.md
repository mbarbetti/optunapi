# OptunAPI

OptunAPI is a simple API designed for Machine Learning applications that allows 
to distribute an automatic hyperparameters optimization over different machines 
through _HTTP requests_. Each set of hyperparameters can be studied independently 
since the minima research does't require any gradients computation, but instead 
is performed through a _Bayesian optimization_ based on [Optuna](https://optuna.org/).
The machine running Optuna manages centrally the optimization studies (_Optuna-server_)
providing sets of hyperparameters and assessing them by the scores evaluated and
sent back by the single computing instance (_Trainer-client_). The HTTP requests
underlying such client-server system are powered by [FastAPI](https://fastapi.tiangolo.com).

## Key Features

OptunAPI inherits most of the modern functionalities of Optuna and FastAPI:

- **Lightweight and versatile**
  - OptunAPI is entirely written in Python and has few dependencies.
- **Easy to configure**
  - For hyperparameters sampling, OptunAPI relies on [configuration files](#configuration-file) easy to set up.
- **Easy to integrate**
  - The hyperparameters values can be easily recover [decoding the HTTP response content](#trainer-client) from the server.
- **Easy parallelization**
  - Different machines can straightforwardly run the hyperparameters study in parallel, centrally coordinated by the server.
- **Efficient optimization algorithms**
  - Optuna enables efficient hyperparameter optimization by adopting state-of-the-art algorithms for sampling hyperparameters.
- **Quick visualization for study analysis**
  - _TODO_ - OptunAPI provides a set of reports based on `optuna.visualization` to monitor the status of the hyperparameters study.

## Basic Concepts

Description of basic concepts.

- spiegare trial e study
- descrivere le due funzioni in server.py
- ask-and-tell interface

## Requirements

Python 3.6+

OptunAPI is based on two modern and highly performant frameworks:

- [Optuna](https://optuna.org/) for the optimization parts.
- [FastAPI](https://fastapi.tiangolo.com) for the HTTP requests parts.

## Installation

bla bla bla

<div class="termy">

```console
$ git clone https://github.com/mbarbetti/optunapi.git

---> 100%
```

</div>

bla bla bla

<div class="termy">

```console
$ pip install optuna fastapi

---> 100%
```

</div>

Standing on the shoulder of FastAPI, OptunAPI needs an ASGI server to run 
the so-called Optuna-server, such as [Uvicorn](https://www.uvicorn.org) 
or [Hypercorn](https://gitlab.com/pgjones/hypercorn).

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Example

### Configuration file

### Optuna-server

Run the server with:

<div class="termy">

```console
$ uvicorn server:optunapi

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>About the command <code>uvicorn server:optunapi</code>...</summary>

The command `uvicorn server:optunapi` refers to:

* `server`: the file `server.py` (the Python "module").
* `optunapi`: the object created inside of `server.py` with the line `optunapi = FastAPI()`.

</details>

### Trainer-client

This is a simple example:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

```YAML
questa : è
una : prova
```

## Securing HTTP requests

## License

This project is licensed under the terms of the MIT license.