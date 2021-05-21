import sshtunnel
import requests


with sshtunnel.open_tunnel (
  (REMOTE_SERVER_IP, 22),
  ssh_username = 'mbarbetti',
  ssh_pkey = '/home/mbarbetti/.ssh/id_rsa',
  remote_bind_address = (PRIVATE_SERVER_IP, PRIVATE_SERVER_PORT),
  local_bind_address  = ('127.0.0.1', 10022)
) as tunnel:
  ping = requests.get ('http://localhost:10022/optunapi/ping')
  ping_msg = ping.json()
  print (ping_msg)