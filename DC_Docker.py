import json
import sys
import docker
from docker import DockerClient
import os
from pprint import pprint
from typing import List, Union
import pickle
import time, datetime
from src.client import Client


def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def create_node(
    client: DockerClient, n: int = 1, node_type: str = "MASTER", port: str = None
) -> Union[List[DockerClient], DockerClient]:
    containers = []
    for _ in range(n):
        container = client.containers.create(
            "dc_docker",
            environment={"NODE_TYPE": node_type},
            volumes={
                config["shared_folder"]: {
                    "bind": "/root/shared/",
                    "mode": "rw",
                },
                "D:/Projects/DC-Docker/src": {
                    "bind": "/root/src/",
                    "mode": "rw",
                },
            },
            detach=True,
            # network_mode="host",
            version="auto",
            # ports={"50007": port} if port is not None else {},
        )
        containers.append(container)
    return containers[0] if n == 1 else containers


if __name__ == "__main__":
    filename = "config.json" if len(sys.argv) == 1 else sys.argv[1]
    config = read_json(filename)

    client = docker.from_env()

    master = create_node(client, 1, "MASTER", "61000")
    clients = create_node(client, config["num_workers"], "WORKER")

    os.remove('./debug/shared/config.pckl')

    master.start()
    master.reload()
    print(master.attrs["NetworkSettings"]["Networks"])
    ip = master.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]

    for client in clients:
        client.start()
        client.reload()

    masteraddr = (master.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"], 50007)
    clientaddrs = {}
    clientaddrs = {c.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]: 50007 for c in clients}
    config = {
        "master_address": masteraddr,
        "worker_addresses": clientaddrs,
        "input_file": config["input_file"],
        "output_file": config["output_file"],
    }

    with open("./debug/shared/config.pckl", "wb") as f:
        f.write(pickle.dumps(config))

    # c = Client("localhost", 61000)
    # c.send("from p")
    # while master.status == "running":
    #     time.sleep(1)
    #     print(datetime.datetime.now().time(), end="\r\t\t\t\r")

    # master.stop()
    # for client in clients:
    #     client.stop()

    # master.remove()
    # for client in clients:
    #     client.remove()
