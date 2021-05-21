import sshtunnel
import requests

with sshtunnel.open_tunnel (
  ('ec2-3-141-165-243.us-east-2.compute.amazonaws.com', 22),
  ssh_username = "mabarbet",
  ssh_pkey = "/home/mabarbet/lb_mabarbet.pem",
  remote_bind_address = ('127.0.0.1', 8000),
  local_bind_address  = ('127.0.0.1', 8040)
) as tunnel:
  pippo = requests.get ('http://localhost:8040/optunapi/ping')
  print (pippo.json())