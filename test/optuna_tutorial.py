import optuna

import os
PATH = os.path.abspath (os.path.dirname (__file__))

import sys
import logging
optuna.logging.get_logger('optuna').addHandler(logging.StreamHandler(sys.stdout))


study_name = '{}/tutorial-study' . format ( os.path.join (PATH, 'db') )
storage_name = 'sqlite:///{}.db' . format ( study_name )
study = optuna . create_study (study_name = study_name, storage = storage_name, load_if_exists = True)

def objective (trial):
  x = trial.suggest_uniform ('x', -10, 10)
  return (x - 2) ** 2

### Hyperparams manually inserted
#study.add_trial (
#  optuna.trial.create_trial (
#    params = {'x': 2.5},
#    distributions = {'x': optuna.distributions.UniformDistribution (-10, 10)},
#    value = 0.25,
#  )
#)

study.optimize (objective, n_trials = 10)

df = study.trials_dataframe (attrs = ('number', 'value', 'params', 'state'))
#print (df)

print ( '\nRESULT AFTER {} TRIALS' . format (len(study.trials)) )
best_params = study.best_params
best_value  = study.best_value
print ( '+--------------------+' )
print ( '|    x      : {:.4f} |' . format (best_params['x']) )
print ( '| (x - 2)^2 : {:.4f} |' . format (best_value) )
print ( '+--------------------+\n' )
