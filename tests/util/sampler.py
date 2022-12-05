import time

from fipy.ngsi.entity import TextAttr, ArrayAttr, FloatAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
import random
from typing import Optional

from ai4sdw.ngsy import WorkerEntity
from tests.util.fiware import orion_client
import numpy as np
import cv2
import base64

class MachineSampler(DevicePoolSampler):

    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())


    def new_device_entity(self) -> WorkerEntity:
        random.seed(time.time())
        n = random.randint(1,10)

        # boxes = ""
        boxes = []
        pose = []

        random.seed(time.time())

        frame = np.zeros(shape=(640,640,3), dtype=np.uint8)
        retval, buffer = cv2.imencode('.jpg', frame)
        text_frame = base64.b64encode(buffer).decode()

        for i in range(n):
            # bbox = f"{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)},{random.randint(0, 100)}"
            # boxes = boxes+bbox
            random.seed(time.time())
            for bi in range(1 * 2): # xy bottom center
                boxes.append(random.randint(0,100))

            random.seed(time.time())
            for ji in range(17 * 2):    # 17 xy coords
                pose.append(random.randint(0,100))

        return WorkerEntity(
            id='',
            warning_area=ArrayAttr.new([20,20,60,20,20,0,60,0]),
            num_obj=FloatAttr.new(n),
            centers=ArrayAttr.new(boxes),
            poses=ArrayAttr.new(pose),
            e_b_t = ArrayAttr.new([1,3,1]),
            area_capacity=FloatAttr.new(5),
            service_type=TextAttr.new("all"),
            src_points=ArrayAttr.new([100, 100, 200, 100, 100, 0, 200, 0]),
            dst_points=ArrayAttr.new([10, 10, 20, 10, 10, 0, 20, 0])


        )