from fipy.ngsi.entity import BaseEntity, FloatAttr, TextAttr, BoolAttr, ArrayAttr
from typing import Optional

class WorkerEntity(BaseEntity):
    """
    type: string, type of entity
    num_obj: number of objects detected
    e_b_t: list [eta, beta, tau]
    area_capacity: max area capacity
    warning_area: list of N pairs of x,y values representing a polygon [x0,y0,x1,y1,x2,y2,...xn,yn]
    bboxes: list of 3 pairs of x,y values representing the bbox coords and the bottom center point in the real world [x_min, y_min, x_max, y_max, x0, y0]
    poses: list of 17 pairs of x,y values representing the human body pose coords
    service_type: string, AI service request, [LineCrossing, FallDetection, PandemicMonitoring] or 'all' to ask all of them
    """
    type = 'ai4sdw_worker'
    warning_area: Optional[ArrayAttr]
    num_obj: Optional[FloatAttr]
    e_b_t: Optional[ArrayAttr]
    area_capacity: Optional[FloatAttr]
    centers: Optional[ArrayAttr]
    poses: Optional[ArrayAttr]
    src_points: Optional[ArrayAttr]
    dst_points: Optional[ArrayAttr]
    service_type:Optional[ TextAttr]
    # frame: ArrayAttr

class LineCrossing(BaseEntity):
    type = 'ai4sdw_LineCrossing_service'
    status: BoolAttr

class FallDetection(BaseEntity):
    type = 'ai4sdw_FallDetection_service'
    status: BoolAttr

class PandemicMonitoring(BaseEntity):
    type = 'ai4sdw_PandemicMonitoring_service'
    status: FloatAttr