from fastapi import FastAPI

optunapi = FastAPI()

@optunapi.get ('/')
async def read_root():
  return {'message' : 'Hello World!'}
