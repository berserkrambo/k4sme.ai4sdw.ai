from ai4sdw.ai import get_services
from tests.util.sampler import MachineSampler


def send_machine_entities():
    print("sending entities")

    sampler = MachineSampler(pool_size=1)
    ent = sampler.make_device_entity(1)
    out_res = get_services(ent)
    a = 0
    # sampler.sample(samples_n=1, sampling_rate=30)



if __name__ == '__main__':
    send_machine_entities()