# OptunAPI

OptunAPI is a simple API designed for Machine Learning applications that allows 
to distribute an automatic hyperparameters optimization over different machines 
through _HTTP requests_. Each set of hyperparameters can be studied independently 
since the minima research does't require any gradients computation, but instead 
is performed through a _Bayesian optimization_ based on [Optuna](https://optuna.org/).
The machine running Optuna manages centrally the optimization studies (_Optuna-server_)
providing sets of hyperparameters and assessing them by the correspondent scores
sent back by the single computing instance (_Trainer-client_).

## Key Features

List of key features:

- First feature
- Second feature

## Basic Concepts

Description of basic concepts.

## Requirements

Python 3.6+

OptunAPI is based on two modern and highly performant frameworks:

- [Optuna](https://optuna.org/) for the optimization parts.
- [FastAPI](https://fastapi.tiangolo.com) for the web parts.

## Installation

<div class = 'termy'>

```console
$ pip install optunapi

---> 100%
```

</div>

Standing on the shoulder of FastAPI, OptunAPI needs an ASGI server 
to run the Optuna-server, such as [Uvicorn](https://www.uvicorn.org) 
or [Hypercorn](https://gitlab.com/pgjones/hypercorn).

<div class = 'termy'>

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Example

This is an example.
