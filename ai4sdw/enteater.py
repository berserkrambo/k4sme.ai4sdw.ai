"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.orion import OrionClient
from typing import List

import ai4sdw.utils as config
import ai4sdw.log as log
from ai4sdw.ngsy import WorkerEntity
from ai4sdw.ai import get_services


def process_update(ctx: FiwareContext, we: List[WorkerEntity]):
    log.going_to_process_updates(ctx, we)
    estimates = [get_services(e) for e in we]
    update_context(ctx, estimates)

def update_context(ctx: FiwareContext,
                   estimates):
    log.going_to_update_context_with_estimates(ctx, estimates)

    orion = OrionClient(config.orion_base_url(), ctx)
    orion.upsert_entities(estimates)
