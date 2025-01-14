import pytest
from api.api_client import PipedriveClient

from faker import Faker


@pytest.fixture(scope="session")
def pd_client():
    """Shared PipedriveClient for all tests."""
    return PipedriveClient()


@pytest.fixture(scope="session")
def faker_instance():
    """Global Faker instance for random test data."""
    return Faker()


@pytest.fixture
def created_person_ids():
    """Track created person IDs to delete them after tests."""
    return []


@pytest.fixture(autouse=True)
def cleanup_persons(pd_client, created_person_ids):
    """After each test, delete any created persons."""
    yield
    for p_id in created_person_ids:
        pd_client.delete_person(p_id)


@pytest.fixture
def created_org(pd_client):
    """If we need an org to attach the person to."""
    org = pd_client.create_organization(name="Test Org for Person")
    yield org
    pd_client.delete_organization(org["id"])
