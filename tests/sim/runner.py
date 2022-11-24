from fipy.docker import DockerCompose

from tests.util.fiware import wait_on_orion, create_subscriptions
from tests.util.sampler import MachineSampler
from requests import post
import random
import time

docker = DockerCompose(__file__)


def bootstrap():
    docker.build_images()
    docker.start()

    wait_on_orion()

    create_subscriptions()
    print("sub created")

def send_machine_entities():
    # sampler = MachineSampler(pool_size=1)
    # sampler.sample(samples_n=1, sampling_rate=5)
    # print(sampler.make_device_entity(1))

    print("start sending entities")
    n = random.randint(0, 10)
    boxes = ""
    for i in range(n):
        bbox = f"{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)}"
        boxes = boxes + bbox
        if i < n - 1:
            boxes = boxes + "-"

    myobj = {'entities': [{'id': 'urn:ngsi-ld:Machine:1', 'type': 'Machine', 'bbox': {'type': 'Text', 'value': boxes}}], 'actionType': 'append'}
    url = 'http://localhost:1026/v2/op/update'
    headers = {"Content-Type": "application/json", "fiware-service": "ai4sdw"}
    x = post(url, json=myobj, headers=headers)
    time.sleep(5)

def run():
    services_running = False
    try:
        bootstrap()
        services_running = True

        print('>>> sending machine entities to Orion...')
        while True:
            send_machine_entities()

    except KeyboardInterrupt:
        if services_running:
            docker.stop()
