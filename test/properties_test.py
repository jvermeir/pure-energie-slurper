from pathlib import Path

import properties


def test_properties_can_be_loaded(mocker):
    mocker.patch("properties.properties_file", Path("test_properties.json"))
    assert ("YOUR EMAIL", properties.email)
    assert ("PASSWORD", properties.password)
    assert ("CONNECTION_ID", properties.connection_id)
    assert ("ACCESS_TOKEN", properties.access_token)
    assert ("YYYY-MM-DD", properties.start_of_data)
