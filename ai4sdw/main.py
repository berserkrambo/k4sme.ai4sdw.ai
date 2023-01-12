from fipy.ngsi.entity import EntityUpdateNotification
from fipy.ngsi.headers import FiwareContext
from fastapi import FastAPI, Header
from typing import Optional

from ai4sdw.enteater import process_update
from ai4sdw.ngsy import WorkerEntity

app = FastAPI()

@app.get('/')
def root():
    return "ai4sdw"

@app.post("/updates")
def post_updates(notification: EntityUpdateNotification,
                 fiware_service: Optional[str] = Header(None),
                 fiware_servicepath: Optional[str] = Header(None),
                 fiware_correlator: Optional[str] = Header(None)):
    ctx = FiwareContext(
        service=str(fiware_service), service_path=str(fiware_servicepath),
        correlator=str(fiware_correlator)
    )

    print(f"Received data {ctx} - {notification}")

    updated_machines = notification.filter_entities(WorkerEntity)
    if updated_machines:
        process_update(ctx, updated_machines)