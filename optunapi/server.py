import os
PATH = os.path.abspath (os.path.dirname (__file__))

from fastapi import FastAPI
optunapi = FastAPI()

import optuna
from optuna.trial._state import TrialState

from typing import Optional
from utils  import suggest_from_config, create_log_file


@optunapi.get ('/optunapi/ping')
async def ping_server():
  """
  Ping Server
  ===========

  Returns the message "The Optuna-server is alive!" if the server is running.

  Parameters
  ----------
    None

  Returns
  -------
    msg : str
      A message witnessing that the server is running.
  """
  msg = 'The Optuna-server is alive!'
  return msg


@optunapi.get ('/optunapi/hparams/{model_name}')
async def read_hparams (model_name: str):
  """
  Read Hyperparameters
  ====================

  When a machine submits a GET request with path `/optunapi/hparams/{model_name}`,
  an Optuna study is created (if it's the first request) or loaded (for any other
  requests) and an ask instance is called. The resulting trial is equipped with a
  set of hyperparameters and encoded to the HTTP response together with the name
  of the optimization session, the trial identifier, the number of running trials 
  and the number of completed trials.

  Parameters
  ----------
    model_name : str (path parameter)
      Name of the optimization session for which one asks for hyperparameters.

  Returns
  -------
    response : dict (HTTP response)
      Dictionary with the following items:
        - `model_name` > Name of the optimization session
        - `trial_id` > Number identifying the created trial
        - `params` > Current set of values for the hyperparameters
        - `running_trials` > Number of running trials
        - `completed_trials` > Number of completed trials
  """
  study_name = os.path.join (PATH, 'db', model_name)
  storage_name = 'sqlite:///{}.db' . format (study_name)
  study = optuna.create_study ( 
                                study_name = study_name ,
                                storage = storage_name  ,
                                load_if_exists = True   ,
                              )
  
  trial = study.ask()

  config_file = '{}/config/{}.yaml' . format (PATH, model_name)
  suggest_from_config (trial, configuration = config_file)

  log_file = '{}/log/{}.log' . format (PATH, model_name)
  create_log_file (study, log_file = log_file)

  running_trials   = study.get_trials (
                                        deepcopy = False,
                                        states = (TrialState.RUNNING,)
                                      )
  completed_trials = study.get_trials (
                                        deepcopy = False,
                                        states = (TrialState.COMPLETE,)
                                      )

  trial_id = study.trials[-1].number
  params   = study.trials[-1].params
  num_running_trials = len (running_trials)
  num_completed_trials = len (completed_trials)

  response = {
               'model_name' : model_name  ,
               'trial_id'   : trial_id    ,
               'params'     : params      ,
               'running_trials' : num_running_trials ,
               'completed_trials' : num_completed_trials ,
             }
  
  return response


@optunapi.get ('/optunapi/score/{model_name}')
async def send_score (
                       model_name : str            ,
                       trial_id   : int            ,
                       score      : float          ,
                     ):
  """
  Send Score
  ==========

  When a machine submits a GET request with path `/optunapi/score/{model_name}?trial_id=TRIAL_ID&score=SCORE`,
  an Optuna study is loaded and its trial `TRIAL_ID` is finished with score `SCORE` calling a tell instance.
  The corresponding HTTP response encodes the name of the optimization session, `TRIAL_ID`, the tested set of
  hyperparameters, `SCORE`, the number identifying the best trial, the best set of hyperparameters, the best 
  score, the number of running trials and the number of completed trials.

  Parameters
  ----------
    model_name : str (path parameter)
      Name of the optimization session for which one asks for hyperparameters.

    trial_id : int (query parameter)
      Number identifying the tested trial.

    score : float (query parameter)
      Score obtained with the set of hyperparameters tested.

  Returns
  -------
    response : dict (HTTP response)
      Dictionary with the following items:
        - `model_name` > Name of the optimization session
        - `trial_id` > Number identifying the tested trial
        - `params` > Tested set of values for the hyperparameters
        - `score` > Score obtained with the tested set of hyperparameters
        - `best_trial_id` > Number identifying the best trial
        - `best_params` > Best set of values for the hyperparameters
        - `best_score` > Score obtained with the best set of hyperparameters
        - `running_trials` > Number of running trials
        - `completed_trials` > Number of completed trials
  """
  study_name = os.path.join (PATH, 'db', model_name)
  storage_name = 'sqlite:///{}.db' . format (study_name)
  study = optuna.create_study ( 
                                study_name = study_name,
                                storage = storage_name,
                                load_if_exists = True
                              )

  study.tell (trial_id, score)

  log_file = '{}/log/{}.log' . format (PATH, model_name)
  create_log_file (study, log_file = log_file)

  running_trials   = study.get_trials (
                                        deepcopy = False,
                                        states = (TrialState.RUNNING,)
                                      )
  completed_trials = study.get_trials (
                                        deepcopy = False,
                                        states = (TrialState.COMPLETE,)
                                      )

  params = study.trials[trial_id].params
  best_trial  = study.best_trial.number
  best_params = study.best_params
  best_score  = study.best_value
  num_running_trials = len (running_trials)
  num_completed_trials = len (completed_trials)

  response = {
               'model_name'  : model_name  ,
               'trial_id'    : trial_id    ,
               'params'      : params      ,
               'score'       : score       ,
               'best_trial'  : best_trial  ,
               'best_params' : best_params ,
               'best_score'  : best_score  ,
               'running_trials' : num_running_trials ,
               'completed_trials' : num_completed_trials ,
             }

  return response
  