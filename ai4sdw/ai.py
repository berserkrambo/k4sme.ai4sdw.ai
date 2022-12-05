import numpy as np
import cv2

from ai4sdw.fall_detector.detect import FallDetector
from ai4sdw.line_crossing.detect import in_hull
from ai4sdw.pandemic_monitoring.detect import get_distance_level
from ai4sdw.ngsy import AI4SDW_services
from fipy.ngsi.entity import BoolAttr, FloatAttr


def get_homograpty_matrix(src_points, dst_points):
    # type: (np.ndarray, np.ndarray) -> np.ndarray
    """
    :param src_points: points coordinates on the image plane
        >> numpy array with shape (N, 2), with N >= 4
    :param dst_points: points coordinates (x3d, y3d) on the real plane with z3d=0
        >> numpy array with shape (N, 2), with N >= 4
    :return: homograpty matrix
        >> numpy array with shape (3, 3)
    """
    homograpty_matrix, _ = cv2.findHomography(src_points, dst_points, method=cv2.RANSAC)
    return homograpty_matrix


def apply_homography(point2d, homograpty_matrix):
    # type: (Union[Sequence[int], np.ndarray], np.ndarray) -> np.ndarray
    """
    Apply the homography transformation to the input 2D point.
    :param point2d: point on the image plane to be transformed.
    :param homograpty_matrix: 3x3 matrix that defines the homography transformation
    :return: transformed point (x3d, y3d) on the real plane with z3d=0
    """
    point2d = point2d.reshape((-1, 1, 2)).astype(np.float32)
    transformed_points = cv2.perspectiveTransform(point2d, homograpty_matrix)
    return transformed_points


def points_to_3d_hom(bottom_center_bbox, h_matrix):
    # type: (Tuple[int, int], np.ndarray) -> List[float]
    """
    :param bottom_center_bbox: bottom center point of a bounding box
    :param h_matrix: homography matrix
    :return: estimated center_points coordinates on the z3d=0 plane
    """
    return apply_homography(point2d=bottom_center_bbox, homograpty_matrix=h_matrix)


def get_services(entity):
    """
    :param entity: WorkerEntity
    :return: List of AI services
    """

    center_points = np.asarray(entity.centers.value, dtype='float').reshape((-1, 1, 2))
    poses = np.asarray(entity.poses.value, dtype='float').reshape((-1, 17, 2))
    res_fall_det = FallDetector().predict(poses=poses, worker=entity)

    h_matrix = get_homograpty_matrix(np.asarray(entity.src_points.value, dtype='float').reshape((-1, 1, 2)),
                                     np.asarray(entity.dst_points.value, dtype='float').reshape((-1, 1, 2)))
    center_points_to_plan = points_to_3d_hom(center_points, h_matrix)
    area_points_to_plan = points_to_3d_hom(np.asarray(entity.warning_area.value, dtype='float').reshape((-1, 1, 2)),
                                           h_matrix)
    res_nonwalk_area = in_hull(center_points_to_plan, polygon=area_points_to_plan, worker=entity)

    eta, beta, tau = entity.e_b_t.value
    res_distances = get_distance_level(center_points_to_plan, eta, beta, tau, entity.area_capacity.value, entity)

    return AI4SDW_services(id=entity.id, area_crossed=BoolAttr.new(res_nonwalk_area),
                           fall_pred=BoolAttr.new(res_fall_det), risk_leve=FloatAttr.new(res_distances))
