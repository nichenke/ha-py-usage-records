"""Tests for the usage records module"""

import pytest

from ha_usage_records.usage_records import UsageRecord


@pytest.fixture
def usage_record(sample_data):
    """Fixture that provides a parsed UsageRecord instance"""
    return UsageRecord.model_validate_json(sample_data)


def military_time(dt):
    """Convert datetime to military time"""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


MT = military_time


def test_usage_record(usage_record):
    """Test UsageRecord parsing"""
    # Now using the fixture instead of parsing SAMPLE directly
    record = usage_record

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
