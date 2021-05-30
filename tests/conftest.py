import pytest

from dolib import AsyncClient, Client


@pytest.fixture(scope="module")
def vcr_config() -> dict:
    def before_record_response(response: dict) -> dict:
        filtered_headers = {}
        for header in response["headers"]:
            if header.lower() in [
                "cf-ray",
                "set-cookie",
                "cf-request-id",
                "x-request-id",
            ]:
                continue
            filtered_headers[header] = response["headers"][header]
        response["headers"] = filtered_headers
        return response

    return {
        "decode_compressed_response": True,
        "filter_headers": ["authorization"],
        #        "record_mode": "rewrite",
        "before_record_response": before_record_response,
    }


@pytest.fixture
def client() -> Client:
    return Client(token="fake_token")


@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(token="fake_token") as async_client:
        return async_client
