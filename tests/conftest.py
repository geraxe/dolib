import pytest


@pytest.fixture(scope="module")
def vcr_config() -> dict:
    return {
        "decode_compressed_response": True,
        "filter_headers": ["authorization"],
        #        "record_mode": "rewrite",
    }
