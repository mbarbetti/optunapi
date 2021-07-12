[![PyPI license](https://img.shields.io/pypi/l/optunapi.svg)](https://pypi.python.org/pypi/optunapi/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/optunapi.svg)](https://pypi.python.org/pypi/optunapi/)
[![PyPI status](https://img.shields.io/pypi/status/optunapi.svg)](https://pypi.python.org/pypi/optunapi/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/optunapi.svg)](https://pypi.python.org/pypi/optunapi/)
[![GitHub issues](https://img.shields.io/github/issues/mbarbetti/optunapi.svg)](https://github.com/mbarbetti/optunapi/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/mbarbetti/optunapi.svg)](https://github.com/mbarbetti/optunapi/pulls/)
[![Downloads](https://pepy.tech/badge/optunapi)](https://pepy.tech/project/optunapi)
[![GitHub stars](https://img.shields.io/github/stars/mbarbetti/optunapi?style=social)](https://github.com/mbarbetti/optunapi)

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
  - the _path_ is `/optuna/score/{model_name}?trail_id=TRIAL_ID&score=SCORE` (with _query parameters_)
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

To run and use OptunAPI it's preferable to create a virtual environment with Python 3.6+ and install Optuna and FastAPI within it.

<div class="termy">

```console
$ pip install optuna fastapi

---> 100%
```

</div>

Standing on the shoulder of FastAPI, OptunAPI needs an ASGI server to run the so-called Optuna-server, 
such as [Uvicorn](https://www.uvicorn.org) or [Hypercorn](https://gitlab.com/pgjones/hypercorn).

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Example

### Configuration file

The high-level functions provided by Optuna [to suggest values for the hyperparameters](#study-and-trial) 
are replaced with an appropriate _configuration file_ in OptunAPI. Referring to the example reported in
the [Optuna tutorial](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html),
what follows is the corresponding YAML configuration file:

```YAML
# Categorical parameter
optimizer:
  name    : optimizer
  type    : categorical
  choices : 
            - RMSprop
            - Adam

# Integer parameter
num_layers:
  name : num_layers
  type : int
  low  : 1
  high : 3

# Integer parameter (log)
num_channels:
  name : num_channels
  type : int
  low  : 32
  high : 52
  log  : True

# Integer parameter (discretized)
num_units:
  name : num_units
  type : int
  low  : 10
  high : 100
  step : 5

# Floating point parameter
dropout_rate:
  name : dropout_rate
  type : float
  low  : 0.0
  high : 1.0

# Floating point parameter (log)
learning_rate:
  name : learning_rale
  type : float
  low  : 1e-5
  high : 1e-2
  log  : True

# Floating point parameter (discretized)
drop_path_rate:
  name : drop_path_rate
  type : float
  low  : 0.0
  high : 1.0
  step : 0.1
```

### Optuna-server

Prepared the configuration file for the optimization session and saved it into 
[`optunapi/optunapi/config`](https://github.com/mbarbetti/optunapi/tree/main/optunapi/config),
we are ready to run the Optuna-server.

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
<summary>What does the command <code>uvicorn server:optunapi</code> mean?</summary>

The command `uvicorn server:optunapi` refers to:

* `server`: the file `server.py` (the Python "module") in 
  [optunapi/optunapi](https://github.com/mbarbetti/optunapi/tree/main/optunapi).
* `optunapi`: the object created inside of `server.py` with the line `optunapi = FastAPI()`.

</details>

Note that Uvicorn sets `127.0.0.1` and `8000` as default values for the server IP and port.
To change the defaults it's enough launching the previous command with the arguments 
`--host` and `--port` followed by the chosen values.

### Trainer-client

The optimization session is managed by an Optuna _study_, initialized with the first client HTTP request, 
or loaded and expanded by any other connecting machines. To refer to a particular optimization session a 
client has to encode the name of the corresponding configuration file within its HTTP request.

Consider the simple use-case provided by OptunAPI, where we want to find the minimum of a 2D-paraboloid:
[`optunapi/tests/simple_client.py`](https://github.com/mbarbetti/optunapi/blob/main/tests/simple_client.py).
Since the provided configuration file is named `optuna-test.yaml`, then the GET request submitted by the client 
to receive the hyperparameters set has to contain the string `'optuna-test'`:

```Python
import requests

HOST = 'http://127.0.0.1:8000'

read_hparams = requests.get (HOST + '/optunapi/hparams/optunapi-test')
hp_req = read_hparams.json()

TRIAL_ID = hp_req ['trial_id']
PARAMS   = hp_req [ 'params' ]
```

What happens behind the scenes is that the above HTTP request calls an _ask_ instance to the Optuna 
_study_, stored in [`optunapi/optunapi/db`](https://github.com/mbarbetti/optunapi/tree/main/optunapi/db) 
once created and named `optunapi-test.db`. As already said, an _ask_ instance is a _trial_ equipped with 
a set of hyperparameters and the client can recover those values decoding the corresponding HTTP response. 
In the example above, `hp_req` is a dictionary containing, among others, the identifier number of the current 
_trial_ (`TRIAL_ID`) and a dictionary for the hyperparameters values (`PARAMS`). 

Having accessed to the hyperparameters values, we can perform whatever learning algorithm one prefers and 
evaluate the associated training score, that will be used as _objective value_ to finish the _trial_ instance.
This is done with a new GET request referring to the same optimization session (again, `'optunapi-test'` in the path) 
and passing `TRIAL_ID` and `SCORE` as query parameters:

```Python
import requests

HOST = 'http://127.0.0.1:8000'

send_score = requests.get (HOST + '/optunapi/score/optunapi-test?trial_id=TRIAL_ID&score=SCORE')
score_req  = send_score.json()

BEST_TRIAL_ID = score_req ['best_score_id']
BEST_PARAMS   = score_req [ 'best_params' ]
```

Each running client allows to refine the search for minima performed by the Optuna algorithms, focusing 
on smaller and smaller space portion and enhancing the mapping of the hyperparameters space.

## Securing HTTP requests

OptunAPI is designed to be used within a VPN not directly opened to the public Internet. On the other hand, 
opening the Optuna-server to Internet allows to exploit easily a wide variety of computing resources, from 
on-premises machines to instances deriving from different cloud computing services (AWS, Azure, GCP, etc.).
Such design raises a security issue since anyone can submit a request to the server or catch its response, 
opening the system to cyberattack.

A possible solution to this issue relies on the SSH protocol. The idea is to set up the Optuna-server
as a _private server_ (from the perspective of `REMOTE SERVER`) not directly visible from the outside 
(`LOCAL CLIENT`’s perspective). This configuration, schematically represented in the sketch below, 
allows a _local client_ to still access the _private server_ passing through the _remote server_ 
authenticating with SSH credentials. 

```
    ----------------------------------------------------------------------

                                |
    -------------+              |    +----------+               +---------
        LOCAL    |              |    |  REMOTE  |               | PRIVATE
        CLIENT   | <== SSH ========> |  SERVER  | <== local ==> | SERVER
    -------------+              |    +----------+               +---------
                                |
                             FIREWALL (only port 22 is open)

    ----------------------------------------------------------------------
```

OptunAPI provides a very simple implementation of this scheme: 
[`optunapi/tests/secured_client.py`](https://github.com/mbarbetti/optunapi/blob/main/tests/secured_client.py).
It is based on [sshtunnel](https://github.com/pahaz/sshtunnel/) and allows to submit a HTTP request to the
_private server_ after having specifying our SSH credentials (`ssh_username`, `ssh_pkey`).

```Python
import sshtunnel
import requests

with sshtunnel.open_tunnel (
  (REMOTE_SERVER_IP, 22),
  ssh_username = 'mbarbetti',
  ssh_pkey = '/home/mbarbetti/.ssh/id_rsa',
  remote_bind_address = (PRIVATE_SERVER_IP, PRIVATE_SERVER_PORT),
  local_bind_address  = ('127.0.0.1', 10022)
) as tunnel:
  ping_server = requests.get ('http://localhost:10022/optunapi/ping')
  ping_msg = ping_server.json()
  print (ping_msg)
```

<details markdown="1">
<summary>How to run the server in this case?</summary>

In this configuration the Optuna-server acts as _private server_, 
then its IP and port are the ones declared within the `with` statement:

```
$ uvicorn server:optunapi --host PRIVATE_SERVER_IP --port PRIVATE_SERVER_PORT
```
</details>

## License

This project is licensed under the terms of the MIT license.
