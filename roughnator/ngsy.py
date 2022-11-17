from fipy.ngsi.entity import BaseEntity, FloatAttr, TextAttr
from typing import Optional


class MachineEntity(BaseEntity):
    type = 'Machine'
    bbox: Optional[TextAttr]


class RoughnessEstimateEntity(BaseEntity):
    type = 'RoughnessEstimate'
    acceleration: FloatAttr
    roughness: FloatAttr

