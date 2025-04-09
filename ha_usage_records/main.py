"""main server for HA Usage Records"""

import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict
from pathlib import Path

from fastapi import FastAPI, Request
import logfire
from .usage_records import UsageRecord

app = FastAPI()

logfire.configure(service_name="ha_usage_records", send_to_logfire=True)
# Uncomment the following lines to enable logging for Pydantic and FastAPI
logfire.instrument_pydantic()
logfire.instrument_fastapi(app, capture_headers=True, capture_query_params=True)


def format_datetime_with_z(dt: datetime) -> str:
    """Format datetime with Z timezone designator for UTC"""
    if dt.tzinfo:
        dt = dt.astimezone(timezone.utc)
    else:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# Ensure records directory exists
RECORDS_DIR = Path("./records")
RECORDS_DIR.mkdir(exist_ok=True)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all incoming requests and save /usage requests to disk"""
    # Generate a unique request ID
    request_id = str(uuid.uuid4())

    # Get the request path and method
    path = request.url.path
    method = request.method

    # Log basic request info
    logfire.info("Request received", request_id=request_id, method=method, path=path)

    # If it's a PUT request to /usage endpoint, save the body
    if path == "/usage" and method == "PUT":
        # Read request body
        body = await request.body()

        try:
            # Try to parse as JSON for prettier storage
            body_json = json.loads(body)

            # Create a timestamped filename for the record
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{request_id}.json"
            file_path = RECORDS_DIR / filename

            # Save the request body to a file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(body_json, f, indent=2)

            logfire.info(
                "Saved usage record", request_id=request_id, file_path=str(file_path)
            )

        except json.JSONDecodeError:
            # If not valid JSON, save raw bytes
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{request_id}.bin"
            file_path = RECORDS_DIR / filename

            with open(file_path, "wb") as f:
                f.write(body)

            logfire.warning(
                "Saved non-JSON usage record",
                request_id=request_id,
                file_path=str(file_path),
            )

    # Process the request
    response = await call_next(request)

    # Log response info
    logfire.info(
        "Response sent", request_id=request_id, status_code=response.status_code
    )

    return response


@app.get("/")
def read_root():
    """Root endpoint that returns a simple greeting"""
    return {"Hello": "World"}


@app.post("/usage")
def put_usage(records: List[UsageRecord]) -> Dict[str, int]:
    """Process multiple usage records and return only the count"""
    # Process the records (you would typically save them to a database here)
    record_count = len(records)

    # Return just the count of records processed
    return {"records_processed": record_count}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
