import time
import random
from fipy.ngsi.entity import FloatAttr, TextAttr, ArrayAttr
from ai4sdw.ai import get_services
from ai4sdw.ngsy import WorkerEntity

def run():
    random.seed(time.time())

    print('>>> sending machine entities to Orion...')
    while True:

        boxes = []
        pose = []

        n = random.randint(1,10)
        for i in range(n):
            random.seed(time.time())
            for bi in range(1 * 2):     # xy bottom center
                boxes.append(random.randint(0, 100))

            random.seed(time.time())
            for ji in range(17 * 2):    # 17 xy coords
                pose.append(random.randint(0, 100))

        to_send = WorkerEntity(
            id=1,   # 'urn:ngsi-ld:ai4sdw_worker:1'
            num_obj=FloatAttr.new(n),
            warning_area=ArrayAttr.new([20,20,60,20,20,0,60,0]),
            centers=ArrayAttr.new(boxes),
            poses=ArrayAttr.new(pose),
            e_b_t=ArrayAttr.new([3,1,3]),
            area_capacity=FloatAttr.new(5),
            service_type=TextAttr.new("all"),
            src_points=ArrayAttr.new([100,100,200,100,100,0,200,0]),
            dst_points=ArrayAttr.new([10,10,20,10,10,0,20,0])
        )

        service_res = get_services([to_send])

        time.sleep(5)


if __name__ == '__main__':
    run()