import requests


HOST = 'http://127.0.0.1:8000'
model_name = 'optunapi-test'

num_trials = 10
for _ in range (num_trials):
  read_hparams = requests.get (HOST + '/optunapi/hparams/{}' . format (model_name))
  hp_req = read_hparams.json()

  trial_id = hp_req [ 'trial_id' ]
  params   = hp_req [  'params'  ]
  running_trials = hp_req [ 'running_trials' ]

  print ( 
    'Trial {} started with parameters: {}. Total number of running trials: {}.' \
    . format ( trial_id, params, running_trials )
        )

  x = params['x']
  y = params['y']
  func = (x - 2) ** 2 + (y - 3) ** 2

  send_score = requests.get (HOST + '/optunapi/score/{}?trial_id={}&score={}' . format (model_name, trial_id, func))
  score_req  = send_score.json()
  
  trial_id    = score_req [  'trial_id'   ]
  score       = score_req [   'score'     ]
  best_trial  = score_req [ 'best_trial'  ]
  best_score  = score_req [ 'best_score'  ]
  best_params = score_req [ 'best_params' ]
  completed_trials = score_req [ 'completed_trials' ]

  print (
    'Trial {} finished with value: {}. Best is trial {} with value: {} and parameters: {}. Total number of completed trials: {}.\n' \
    . format ( trial_id, score, best_trial, best_score, best_params, completed_trials )
        )

print ( '\nRESULT AFTER {} TRIALS' . format (completed_trials) )
print ( '+--------------------------------+' )
print ( '|           x           : {:.4f} |' . format (best_params['x']) )
print ( '|           y           : {:.4f} |' . format (best_params['y']) )
print ( '| (x - 2)^2 + (y - 3)^2 : {:.4f} |' . format (best_score)       )
print ( '+--------------------------------+\n' )
