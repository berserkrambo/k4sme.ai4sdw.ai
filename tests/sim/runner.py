from fipy.docker import DockerCompose

from tests.util.fiware import wait_on_orion, create_subscriptions
from tests.util.sampler import MachineSampler


docker = DockerCompose(__file__)


def bootstrap():
    docker.build_images()
    docker.start()

    wait_on_orion()

    create_subscriptions()
    print("sub created")


def send_machine_entities():
    print("sending entities")

    sampler = MachineSampler(pool_size=1)
    sampler.sample(samples_n=1, sampling_rate=5)
    print(sampler.make_device_entity(1))


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
