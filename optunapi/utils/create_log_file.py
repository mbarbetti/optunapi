from optuna.study import Study


def create_log_file (study: Study, log_file: str):
  """
  Create Log File
  ===============

  Allows to create a log file containing a pandas `DataFrame` of trials in the `Study`.

  Parameters
  ----------
    study : optuna.study.Study
      Set of `Trial` objects deriving from an Ask-and-Tell interface.

    log_file : str
      Name of file reporting the study results.

  Returns
  -------
    None
  """
  df = study.trials_dataframe ( attrs = ('number', 'params', 'value', 'state') )
  with open (log_file, 'w') as file:
    print (df.to_string(), file = file)
