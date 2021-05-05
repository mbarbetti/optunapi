import optuna

def function (trial):
  x = trial.suggest_uniform ('x', -10, 10)
  return (x - 2) ** 2

study = optuna.create_study()
study.optimize (function, n_trials = 100)

study.best_params
