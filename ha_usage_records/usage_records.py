""" Usage Records for 1nce

Ref: https://help.1nce.com/dev-hub/docs/data-streamer-usage-records
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrganizationRecord(BaseModel):
    """Organization Fields"""

    name: str
    id: int


class SimRecord(BaseModel):
    """Sim Fields"""

    msisdn: str
    iccid: str
    id: int
    production_date: datetime


class OperatorRecord(BaseModel):
    """Operator Fields"""

    id: int
    name: str
    mnc: str
    country: dict


class EndpointRecord(BaseModel):
    """Endpoint Fields"""

    tags: Optional[str] = None
    ip_address: str
    name: str
    imei: str
    id: int
    balance: Optional[str] = None


class VolumeRecord(BaseModel):
    """Volume Fields"""

    total: float
    tx: float
    rx: float


class UsageRecord(BaseModel):
    """1nce Usage Record"""

    id: int
    imsi: str
    organisation: OrganizationRecord
    start_timestamp: datetime
    sim: SimRecord
    operator: OperatorRecord
    imsi_id: int
    end_timestamp: datetime
    endpoint: EndpointRecord
    cost: float
    volume: VolumeRecord
