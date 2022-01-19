from server import Server
from client import Client
import pickle
import math
import json
from typing import Dict, List
import os
import sys
from pprint import pprint
import time
import socket

# with open("./shared/output.txt", "w") as f:
#     f.write("hello there from master1")
print("inside server")
# _, master_port = config["master_address"]
local_ip = socket.gethostbyname(socket.gethostname())
print(local_ip)
s = Server("0.0.0.0", 50007)
c = Client()
print("inside server2")
sys.stdout.flush()
# r = s.recieve()
# print("recieved", r)

with open("./shared/output.txt", "w") as f:
    f.write("hello there from master2")

# get from shared folder.
while not os.path.isfile("./shared/config.pckl"):
    continue
with open("./shared/config.pckl", "rb") as f:
    config = pickle.loads(f.read())
filename = os.path.join("./shared", config["input_file"])
pprint(config)
sys.stdout.flush()
worker_addresses: Dict = config["worker_addresses"]


def read_lines(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return f.read().splitlines()


lines = read_lines(filename)

num_workers = len(worker_addresses)
optimum_chunk_size = math.ceil(len(lines) / num_workers)
worker_portions = [lines[i : i + optimum_chunk_size] for i in range(0, len(lines), optimum_chunk_size)]

for ip, data in zip(worker_addresses, worker_portions):
    c.connect(ip, worker_addresses[ip])
    c.send(data)
    c.close()

all_data = {}
for _ in worker_addresses:
    data, _ = s.recieve()
    all_data = all_data | data

s.close()
c.close()

filename = os.path.join("./shared", config["output_file"])
with open(filename, "w") as f:
    f.write(json.dumps(all_data))
