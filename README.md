# OptunAPI

OptunAPI is a simple API designed for Machine Learning applications that allows to distribute an automatic 
hyperparameters optimization over different machines through _HTTP requests_. Each set of hyperparameters 
can be studied independently since the minima research does't require any gradients computation, but instead 
is performed through a _Bayesian optimization_ based on [Optuna](https://optuna.org/). The machine running 
Optuna manages centrally the optimization studies (_Optuna-server_) providing sets of hyperparameters and 
assessing them by the scores evaluated and sent back by the single computing instance (_Trainer-client_). 
The HTTP requests underlying such client-server system are powered by [FastAPI](https://fastapi.tiangolo.com).

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
- Optuna's Ask-and-Tell interface
- HTTP requests to map the hyperparameters space

### Study and Trial

A _study_ corresponds to an optimization task, i.e., a set of trials. This object provides interfaces to run a new
[`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)
and access trials' history. OptunAPI is designed so that, when the first machine ask for a hyperparameters set, it
starts a new study ([`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study)) identified according to the HTTP request submitted. Any other machines referring 
to the same optimization session don't initialize a new study, but recover the previous one ([`load_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.load_study.html#optuna.study.load_study)) contributing 
to mapping the hyperparameters space.

A _trial_ allows to prepare a particular set of hyperparameters and evaluate its capability of optimizing a objective
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

The Optuna's _Ask-and-Tell_ interface provides a more flexible interface for hyperparameter optimization
based on the two following methods:

- [`optuna.study.Study.ask()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.ask) creates a trial that can sample hyperparameters
- [`optuna.study.Study.tell()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.tell) finishes the trial by passing `trial` and an objective value

OptunAPI uses these methods in two different moments. When a machine ask for a set of hyperparameters,
that set belongs to a trial resulting from an _ask_ instance. Then, once the objective function was
evaluated with that particular set of hyperparameters, the machine sends a new request encoding the
objective value allowing to close the corresponding trial with a _tell_ instance.

### HTTP Requests

OptunAPI provides a simple Python module to run a server able to centrally manage the optimization studies:
[`optuna/optuna/server.py`](https://github.com/mbarbetti/optunapi/blob/main/optunapi/server.py). It is
equipped with a set of _path operation functions_ relying on the FastAPI ecosystem:

- `ping_server`
  - the _path_ is `/optunapi/ping`
  - the _operation_ is `GET`
  - the _function_ allows to verify if the server is running
- `read_hparams`
  - the _path_ is `/optuna/hparams/{model_name}` (`model_name` is a _path parameter_)
  - the _operation_ is `GET`
  - the _function_ allows to start (or load) an Optuna study and send sets of hyperparameters
- `send_score`
  - the _path_ is `/optuna/score/{model_name}?trail_id=TRIAL_ID&score=SCORE`
  - the _operation_ is `GET`
  - the _function_ allows to finish the trial identified by `trial_id` with the `score` value

## Requirements

Python 3.6+

OptunAPI is based on two modern and highly performant frameworks:

- [Optuna](https://optuna.org/) for the optimization parts.
- [FastAPI](https://fastapi.tiangolo.com) for the HTTP requests parts.

## Installation

OptunAPI is a [public repository](https://github.com/mbarbetti/optunapi) on GitHub.

<div class="termy">

```console
$ git clone https://github.com/mbarbetti/optunapi.git

---> 100%
```

</div>

To run and use OptunAPI we should create a virtual environment with Python 3.6+ and install Optuna and FastAPI.

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

```YAML
x :
  name    : x
  type    : float
  choices : 
  low     : -10
  high    :  10
  step    :
  log     : False

y :
  name    : y
  type    : float
  choices :
  low     : -10
  high    :  10
  step    :
  log     : False
```

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
import requests


HOST = 'http://127.0.0.1:8000'
model_name = 'optunapi-test'

num_trials = 10
for _ in range (num_trials):
  read_hparams = requests.get (HOST + '/optunapi/hparams/{}' . format (model_name))
  hp_resp = read_hparams.json()

  trial_id   = hp_resp [ 'trial_id' ]
  params     = hp_resp [  'params'  ]
  running_trials = hp_resp [ 'running_trials' ]

  print ( 
    'Trial {} started with parameters: {}. Total number of running trials: {}.' \
    . format ( trial_id, params, running_trials )
        )

  x = params [ 'x' ]
  y = params [ 'y' ]
  func = (x - 2) ** 2 + (y - 3) ** 2

  send_score = requests.get (HOST + '/optunapi/score/{}?trial_id={}&score={}' . format (model_name, trial_id, func))
  score_resp = send_score.json()
  
  trial_id    = score_resp [  'trial_id'   ]
  score       = score_resp [    'score'    ]
  best_trial  = score_resp [ 'best_trial'  ]
  best_score  = score_resp [ 'best_score'  ]
  best_params = score_resp [ 'best_params' ]
  completed_trials = score_resp [ 'completed_trials' ]

  print (
    'Trial {} finished with value: {}. Best is trial {} with value: {} and parameters: {}. Total number of completed trials: {}.\n' \
    . format ( trial_id, score, best_trial, best_score, best_params, completed_trials )
        )

print ( '\nRESULT AFTER {} TRIALS' . format (completed_trials) )
print ( '+--------------------------------+' )
print ( '|           x           : {:.4f} |' . format (best_params['x']) )
print ( '|           y           : {:.4f} |' . format (best_params['y']) )
print ( '| (x - 2)^2 + (y - 3)^2 : {:.4f} |' . format (best_score) )
print ( '+--------------------------------+\n' )
```

## Securing HTTP requests

## License

This project is licensed under the terms of the MIT license.