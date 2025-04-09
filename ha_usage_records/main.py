"""main server for HA Usage Records"""

from fastapi import FastAPI
import logfire
from .usage_records import UsageRecord
from datetime import datetime, timezone

app = FastAPI()

logfire.configure()
# logfire.instrument_pydantic()
logfire.instrument_fastapi(app)


def format_datetime_with_z(dt: datetime) -> str:
    """Format datetime with Z timezone designator for UTC"""
    if dt.tzinfo:
        dt = dt.astimezone(timezone.utc)
    else:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.put("/usage")
def put_usage(record: UsageRecord):
    return {
        "record.id": record.id,
        "record.start_timestamp": format_datetime_with_z(record.start_timestamp),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
