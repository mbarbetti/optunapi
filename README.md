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
  - Different machines can run the hyperparameters study in parallel, centrally coordinated by the server.
- **Efficient optimization algorithms**
  - The optimization task is headed by Optuna and its state-of-the-art algorithms.
- **Quick visualization for study analysis**
  - _TODO_ - OptunAPI provides a set of reports to monitor the status of the hyperparameters study.

## Key Components

To understand how OptunAPI works, we need to spend a couple of words about its components:

- [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) and
  [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial) objects
  from Optuna
- Optuna's _Ask-and-Tell_ interface
- HTTP requests to map the hyperparameters space

### Study and Trial

A _study_ corresponds to an optimization task, i.e., a set of trials. This object provides interfaces to run a new
[`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)
and access trials' history. OptunAPI is designed so that, when the first machine ask for a hyperparameters set, it
starts a new study ([`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study)) identified according to the HTTP request submitted. Any other machines referring 
to the same optimization session don't initialize a new study, but recover the previous one ([`load_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.load_study.html#optuna.study.load_study)) contributing 
to mapping the hyperparameters space.

A _trial_ allows to prepare a particular set of hyperparameters and evaluate its capability of optimizing a target
function, not necessarily available in an explicit form as in the case of very complex Machine Learning algorithms.
This object provides the following interfaces to get parameter suggestion: 

- [`optuna.trial.Trial.suggest_categorical()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.suggest_categorical) for categorical parameters
- [`optuna.trial.Trial.suggest_int()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.suggest_int) for integer parameters
- [`optuna.trial.Trial.suggest_float()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.suggest_float) for floating point parameters

With optional arguments of `step` and `log`, we can discretize or take the logarithm of integer and floating point parameters.
The following code block is taken from the [Optuna tutorial](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html) and shows a standard use of these features:

```Python
import optuna


def objective (trial):
    # Categorical parameter
    optimizer = trial.suggest_categorical ('optimizer', ['RMSprop', 'Adam'])

    # Integer parameter
    num_layers = trial.suggest_int ('num_layers', 1, 3)

    # Integer parameter (log)
    num_channels = trial.suggest_int ('num_channels', 32, 512, log = True)

    # Integer parameter (discretized)
    num_units = trial.suggest_int ('num_units', 10, 100, step = 5)

    # Floating point parameter
    dropout_rate = trial.suggest_float ('dropout_rate', 0.0, 1.0)

    # Floating point parameter (log)
    learning_rate = trial.suggest_float ('learning_rate', 1e-5, 1e-2, log = True)

    # Floating point parameter (discretized)
    drop_path_rate = trial.suggest_float ('drop_path_rate', 0.0, 1.0, step = 0.1)
```

OptunAPI uses these methods internally and requires only a [configuration file](#configuration-file) 
correctly filled to run the studies.

### Ask-and-Tell Interface

bla bla bla

### HTTP Requests

bla bla bla

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

* `server`: the file `server.py` (the Python "module") in [optunapi/optunapi](https://github.com/mbarbetti/optunapi/tree/main/optunapi).
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