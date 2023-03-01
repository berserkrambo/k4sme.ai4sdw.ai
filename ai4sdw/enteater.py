"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.orion import OrionClient
from typing import List

import ai4sdw.utils as config
from ai4sdw.ngsy import WorkerEntity
from ai4sdw.ai import get_services


def process_update(ctx: FiwareContext, we: List[WorkerEntity]):
    estimates = [get_services(e) for e in we if len(e.centers.value) > 0]
    if len(estimates) > 0:
        update_context(ctx, estimates)


def update_context(ctx: FiwareContext,
                   estimates):
    print(f"sending back to orion to update {ctx} - {estimates}")
    orion = OrionClient(config.orion_base_url(), ctx)
    orion.upsert_entities(estimates)
