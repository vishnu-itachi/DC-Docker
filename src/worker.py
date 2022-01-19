from server import Server
from client import Client
from collections import Counter
from pprint import pprint
from typing import List, Dict
import pickle
import socket
import os


def process_lines(lines: List[str]) -> Dict:
    frequency_dict = {}
    for line in lines:
        f_dict = Counter(line)
        frequency_dict = frequency_dict | f_dict
    return frequency_dict


if __name__ == "__main__":
    while not os.path.isfile("./shared/config.pckl"):
        continue
    with open("./shared/config.pckl", "rb") as f:
        config = pickle.loads(f.read())
    pprint(config)
    # # Get the port from config
    # worker_addresses: Dict = config["worker_addresses"]
    local_ip = socket.gethostbyname(socket.gethostname())
    print(local_ip)
    s = Server("0.0.0.0", 50007)
    # s.recieve()
    master_ip, master_port = config["master_address"]

    lines, _ = s.recieve(2 ** 20)
    s.close()
    print(lines)
    frequency_dict = process_lines(lines)
    c = Client(master_ip, 50007)
    c.send(frequency_dict)

    c.close()
