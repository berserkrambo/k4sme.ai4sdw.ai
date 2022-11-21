from fipy.ngsi.entity import TextAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
import random
from typing import Optional

from roughnator.ngsy import MachineEntity
from tests.util.fiware import orion_client


class MachineSampler(DevicePoolSampler):

    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())


    def new_device_entity(self) -> MachineEntity:
        n = random.randint(0,10)

        boxes = ""
        for i in range(n):
            bbox = f"{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)}"
            boxes = boxes+bbox
            if i < n-1:
                boxes = boxes+"-"


        return MachineEntity(
            id='',
            bbox=TextAttr.new(boxes),
        )