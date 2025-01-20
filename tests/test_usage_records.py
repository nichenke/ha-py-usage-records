from ha_usage_records.usage_records import UsageRecord

import pytest

SAMPLE = """
{
    "imsi": "<imsi>",
    "organisation": {
        "name": "8100xxxx",
        "id": 1234
    },
    "start_timestamp": "2021-08-09T12:59:05Z",
    "sim": {
        "msisdn": "<msisdn>",
        "iccid": "<icc>",
        "id": 123456,
        "production_date": "2018-04-17T15:01:50Z"
    },
    "currency": {
        "id": 1,
        "symbol": "€",
        "code": "EUR"
    },
    "operator": {
      "id": 2,
      "name": "T-Mobile",
      "mnc": "01",
      "country": {
        "id": 74,
        "mcc": "262",
        "name": "Germany"
      }
	},
    "tariff": {
        "ratezone": {
            "name": "Rate Zone 2 (EU - DE)",
            "id": 2067
        },
        "name": "1NCE Production 01",
        "id": 398
    },
    "imsi_id": 1234567,
    "traffic_type": {
        "description": "Data",
        "id": 5
    },
    "id": 1234567890,
    "end_timestamp": "2021-08-09T12:51:20Z",
    "endpoint": {
        "tags": null,
        "ip_address": "<ip_address>",
        "name": "<name>",
        "imei": "<imei>",
        "id": 12345678,
				"balance": null
    },
    "cost": 0.001176,
    "volume": {
        "total": 0.001176,
        "tx": 0.001176,
        "rx": 0.0
    }
}
"""


def military_time(dt):
    """convert datetime to military time"""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


MT = military_time


def test_usage_record():
    """test UsageRecord"""
    record = UsageRecord.model_validate_json(SAMPLE)
    assert record.id == 1234567890
    assert record.imsi == "<imsi>"
    assert record.imsi_id == 1234567

    assert record.organisation.name == "8100xxxx"
    assert record.organisation.id == 1234
    assert MT(record.start_timestamp) == "2021-08-09T12:59:05Z"

    assert record.sim.msisdn == "<msisdn>"
    assert record.sim.iccid == "<icc>"
    assert record.sim.id == 123456
    assert MT(record.sim.production_date) == "2018-04-17T15:01:50Z"

    assert record.operator.id == 2
    assert record.operator.name == "T-Mobile"
    assert record.operator.mnc == "01"
    assert record.operator.country["id"] == 74
    assert record.operator.country["mcc"] == "262"
    assert record.operator.country["name"] == "Germany"

    assert record.endpoint.tags is None
    assert record.endpoint.ip_address == "<ip_address>"
    assert record.endpoint.name == "<name>"
    assert record.endpoint.imei == "<imei>"
    assert record.endpoint.id == 12345678
    assert record.endpoint.balance is None

    assert record.cost == 0.001176

    assert record.volume.total == 0.001176
    assert record.volume.tx == 0.001176
    assert record.volume.rx == 0.0
