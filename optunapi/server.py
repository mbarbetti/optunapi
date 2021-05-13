import os
PATH = os.path.abspath (os.path.dirname (__file__))

import optuna
from optuna.trial._state import TrialState

from fastapi import FastAPI
from typing  import Optional

from utils import suggest_from_config, create_log_file



optunapi = FastAPI()


##########################
##  Read hyperparameters
##########################
@optunapi.get ('/optunapi/hparams/{model_name}')
async def read_hparams (model_name: str):
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

  trial_id = study.trials[-1].number
  params   = study.trials[-1].params
  running_trials = study.get_trials (
                                      deepcopy = False,
                                      states = (TrialState.RUNNING,)
                                    )
  num_running_trials = len(running_trials)

  response = {
               'model_name' : model_name  ,
               'trial_id'   : trial_id    ,
               'params'     : params      ,
               'running_trials' : num_running_trials ,
             }
  
  return response


################
##  Send score
################
@optunapi.get ('/optunapi/score/{model_name}')
async def send_score (
                       model_name : str            ,
                       trial_id   : int            ,
                       score      : float          ,
                       step : Optional[int] = None ,
                     ):
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

  params = study.trials[trial_id].params
  best_trial  = study.best_trial.number
  best_params = study.best_params
  best_score  = study.best_value
  completed_trials = study.get_trials (
                                        deepcopy = False,
                                        states = (TrialState.COMPLETE,)
                                      )
  num_completed = len(completed_trials)

  response = {
               'model_name'  : model_name  ,
               'trial_id'    : trial_id    ,
               'params'      : params      ,
               'score'       : score       ,
               'step'        : step        ,
               'best_trial'  : best_trial  ,
               'best_params' : best_params ,
               'best_score'  : best_score  ,
               'completed_trials' : num_completed ,
             }

  return response
  