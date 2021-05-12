import optuna

import os
PATH = os.path.abspath (os.path.dirname (__file__))

import sys
import logging
optuna.logging.get_logger('optuna').addHandler(logging.StreamHandler(sys.stdout))


study_name = '{}/test-study'     . format ( os.path.join (PATH, 'db') )
storage_name = 'sqlite:///{}.db' . format ( study_name )
study = optuna . create_study (study_name = study_name, storage = storage_name, load_if_exists = True)

n_trials = 10
for _ in range (n_trials):
  trial = study.ask()
  
  x   = trial.suggest_uniform ('x', -10, 10)
  val = (x - 2) ** 2

  study.tell (trial, val)

print ( '\nRESULT AFTER {} TRIALS' . format (len(study.trials)) )
best_params = study.best_params
best_value  = study.best_value
print ( '+--------------------+' )
print ( '|    x      : {:.4f} |' . format (best_params['x']) )
print ( '| (x - 2)^2 : {:.4f} |' . format (best_value) )
print ( '+--------------------+\n' )
