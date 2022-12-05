from fipy.ngsi.entity import EntityUpdateNotification
from fipy.ngsi.headers import FiwareContext
import logging
from typing import Any, List

from ai4sdw.ngsy import WorkerEntity


def _logger() -> logging.Logger:
    return logging.getLogger(__name__)


def _format_mgs(lines: List[Any]) -> str:
    ls = [f"{line}\n" for line in lines]
    return ''.join(ls)


def info(msg: str):
    print(msg)


def received_ngsi_entity_update(ctx: FiwareContext,
                                notification: EntityUpdateNotification):
    header = f"got entity updates for {ctx}:"
    msg = _format_mgs([header] + notification.data)
    info(msg)


def going_to_process_updates(ctx: FiwareContext, ms: List[WorkerEntity]):
    header = f"going to process updates for {ctx}:"
    msg = _format_mgs([header] + ms)
    info(msg)


def going_to_update_context_with_estimates(ctx: FiwareContext,
                                           rs):
    header = f"going to update context ({ctx}) with estimates:"
    msg = _format_mgs([header] + rs)
    info(msg)
