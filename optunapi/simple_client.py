import optuna
import requests


HOST = 'http://127.0.0.1:8000'
model_name = 'optunapi-test'

num_trials = 10
for _ in range (num_trials):
  read_hparams = requests.get (HOST + '/optunapi/hparams/{}' . format (model_name))
  hp_resp = read_hparams.json()

  model_name = hp_resp [ 'model_name' ]
  trial_id   = hp_resp [ 'trial_id'   ]
  params     = hp_resp [ 'params'     ]
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
  
  model_name  = score_resp [ 'model_name'  ]
  trial_id    = score_resp [ 'trial_id'    ]
  params      = score_resp [ 'params'      ]
  score       = score_resp [ 'score'       ]
  step        = score_resp [ 'step'        ]
  best_trial  = score_resp [ 'best_trial'  ]
  best_params = score_resp [ 'best_params' ]
  best_score  = score_resp [ 'best_score'  ]
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
