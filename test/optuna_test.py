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

  last_trial     = study.get_trials()[-1]
  trial_num      = last_trial.number
  trial_val      = last_trial.values[0]
  trial_params   = last_trial.params
  best_trial_num = study.best_trial.number
  best_trial_val = study.best_value
  print (
          'Trial {} finished with value: {} and parameters: {}. Best is trial {} with value: {}.' \
          . format ( trial_num, trial_val, trial_params, best_trial_num, best_trial_val )
        )

  ### Multiple trials
  #trial_1 = study.ask()
  #x_1   = trial_1.suggest_uniform ('x', -10, 10)
  #val_1 = (x_1 - 2) ** 2
  #study.tell (trial_1, val_1)
  #
  #trial_2 = study.ask()
  #x_2   = trial_2.suggest_uniform ('x', -10, 10)
  #val_2 = (x_2 - 2) ** 2
  #study.tell (trial_2, val_2)

print ( '\nRESULT AFTER {} TRIALS' . format (len(study.trials)) )
best_params = study.best_params
best_value  = study.best_value
print ( '+--------------------+' )
print ( '|    x      : {:.4f} |' . format (best_params['x']) )
print ( '| (x - 2)^2 : {:.4f} |' . format (best_value) )
print ( '+--------------------+\n' )
