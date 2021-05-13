import yaml
from optuna.trial import Trial


def suggest_from_config (trial: Trial, configuration: str):
  """
  Suggest From Config
  ===================

  Allows to generalize the `suggest_*` functions taking 
  information from a YAML configuration file.

  Parameters
  ----------
    trial : optuna.trial.Trial
      Trial object deriving from an Ask-and-Tell interface.

    configuration : str
      YAML file containing hyperparameters configuration.

  Returns
  -------
    None
  """
  with open (configuration) as file:
    params = yaml.full_load (file)

  for par in params.values():
    if par['type'] == 'categorical':
      trial.suggest_categorical (
                                  name    = par [ 'name'    ] ,
                                  choices = par [ 'choices' ] ,
                                )
    elif par['type'] == 'float':
      trial.suggest_float (
                            name = par [ 'name' ] ,
                            low  = par [ 'low'  ] ,
                            high = par [ 'high' ] ,
                            step = par [ 'step' ] if par [ 'step' ] else None  ,
                            log  = par [ 'log'  ] if par [ 'log'  ] else False ,
                          )
    elif par['type'] == 'int':
      trial.suggest_int (
                          name = par [ 'name' ] ,
                          low  = par [ 'low'  ] ,
                          high = par [ 'high' ] ,
                          step = par [ 'step' ] if par [ 'step' ] else 1     ,
                          log  = par [ 'log'  ] if par [ 'log'  ] else False ,
                        )
    else:
      raise ValueError ('Trial suggestion not implemented.')
