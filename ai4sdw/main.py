from fipy.ngsi.entity import EntityUpdateNotification
from fipy.ngsi.headers import FiwareContext
from fastapi import FastAPI, Header
from typing import Optional

from ai4sdw import __version__
from ai4sdw.enteater import process_update
import ai4sdw.log as log
from ai4sdw.ngsy import WorkerEntity

app = FastAPI()

@app.get('/')
def read_root():
    return {'ai4sdw': __version__}

@app.get("/version")
def read_version():
    return read_root()

@app.post("/updates")
def post_updates(notification: EntityUpdateNotification,
                 fiware_service: Optional[str] = Header(None),
                 fiware_servicepath: Optional[str] = Header(None),
                 fiware_correlator: Optional[str] = Header(None)):
    ctx = FiwareContext(
        service=str(fiware_service), service_path=str(fiware_servicepath),
        correlator=str(fiware_correlator)
    )

    log.received_ngsi_entity_update(ctx, notification)

    updated_machines = notification.filter_entities(WorkerEntity)
    if updated_machines:
        process_update(ctx, updated_machines)