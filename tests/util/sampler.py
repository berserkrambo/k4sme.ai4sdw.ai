from fipy.ngsi.entity import FloatAttr, TextAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
import random
from typing import Optional

from roughnator.ngsy import MachineEntity
from tests.util.fiware import orion_client
from roughnator.ngsy import ListAttr
import json

class MachineSampler(DevicePoolSampler):

    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())

    # def new_device_entity(self) -> MachineEntity:
    #     seed = random.uniform(0, 1)
    #     return MachineEntity(
    #         id='',
    #         AcelR=FloatAttr.new(1.0335 + seed),
    #         fz=FloatAttr.new(0.98201 + seed),
    #         Diam=FloatAttr.new(0.98201 + seed),
    #         ae=FloatAttr.new(1.0335 + seed),
    #         HB=FloatAttr.new(145 + seed),
    #         geom=FloatAttr.new(-0.021 + seed),
    #         Ra=FloatAttr.new(seed)
    #     )

    # def new_device_entity(self) -> MachineEntity:
    #     seed = random.uniform(0, 1)
    #     return MachineEntity(
    #         id='',
    #         x1=FloatAttr.new(1.0335 + seed),
    #         y1=FloatAttr.new(0.98201 + seed),
    #         x2=FloatAttr.new(0.98201 + seed),
    #         y2=FloatAttr.new(1.0335 + seed),
    #     )

    # def new_device_entity(self) -> MachineEntity:
    #     x1 = random.uniform(0, 1)
    #     y1 = random.uniform(0, 1)
    #     x2 = random.uniform(0, 1)
    #     y2 = random.uniform(0, 1)
    #     return MachineEntity(
    #         id='',
    #         bbox=ListAttr.new([x1,y1,x2,y2]),
    #     )

    def new_device_entity(self) -> MachineEntity:
        seed = random.uniform(0, 1)
        n = random.randint(0,10)

        # boxes = []
        # for i in range(n):
        #     bbox = [("x1", random.randint(0, 100)), (")y1", random.randint(0, 100)), ("x2", random.randint(0, 100)),
        #             ("y2", random.randint(0, 100))]
        #     boxes.append(dict(bbox))
        # data = {"nobj": n, "obj": boxes}

        boxes = ""
        for i in range(n):
            bbox = f"{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)}"
            boxes = boxes+bbox
            if i < n-1:
                boxes = boxes+"-"
        # data = {"nobj": n, "obj": boxes}

        return MachineEntity(
            id='',
            bbox=TextAttr.new(boxes),
        )