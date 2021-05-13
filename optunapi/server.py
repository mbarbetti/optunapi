from fastapi import FastAPI
from typing  import Optional

optunapi = FastAPI()

@optunapi.get ('/optunapi/hparams/{model_name}')
async def read_hparams (model_name: str):
  info = model_name . split ('_')
  model    = info[0]
  sample   = info[1]
  particle = info[2]
  return {
           'model'    : model    ,
           'sample'   : sample   ,
           'particle' : particle ,
         }

@optunapi.get ('/optunapi/score/{model_name}')
async def send_score (
                       model_name : str   ,
                       score      : float ,
                       step : Optional[int] = None ,
                     ):
  info = model_name . split ('_')
  model    = info[0]
  sample   = info[1]
  particle = info[2]
  version  = info[3]
  return {
           'model'    : model    ,
           'sample'   : sample   ,
           'particle' : particle ,
           'version'  : version  ,
           'score'    : score    ,
           'step'     : step     ,
         }
  