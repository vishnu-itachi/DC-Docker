import json
import sys
import docker
import os
from pprint import pprint

def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    filename = "config.json" if len(sys.argv) == 1 else sys.argv[1]
    config = read_json(filename)

    client = docker.from_env()
    # api_client = docker.APIClient(base_url='npipe:////./pipe/docker_engine')
    # if "build" in config and config["build"]:
    #     print("starting build")
    #     # client.images.build(path=".", tag="dc_docker")
    #     _ = api_client.build(path=".", dockerfile="Dockerfile", tag="dc_docker:latest")
    #     print([i for i in _])
    #     print("build completed")
        

    container = client.containers.run(
        "dc_docker",
        # remove=True,
        environment=config["environment"],
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
    )
    pprint(container.logs().decode("utf-8") )

