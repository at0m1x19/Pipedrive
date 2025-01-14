import pytest
import requests


def test_create_person_all_params(pd_client, created_person_ids, created_org, faker_instance):
    """Creates a person using all possible parameters."""
    name = faker_instance.name()
    email = [
        {"label": "work", "value": faker_instance.email(), "primary": True},
        {"label": "home", "value": faker_instance.email(), "primary": False}
    ]
    phone = [
        {"label": "mobile", "value": faker_instance.phone_number(), "primary": True},
        {"label": "work", "value": faker_instance.phone_number(), "primary": False}
    ]
    labels = [14, 16]
    org_id = created_org["id"]

    result = pd_client.create_person(
        name=name,
        email=email,
        phone=phone,
        label_ids=labels,
        org_id=org_id
    )
    person_id = result["id"]
    created_person_ids.append(person_id)

    assert result["name"] == name, "Name should match"

    assert result["org_id"]["value"] == org_id, \
        f"Org ID should match (expected {org_id}, got {result['org_id']['value']})"

    assert result["label_ids"] == labels, f"Labels should match (expected {labels}, got {result['label_ids']})"

    assert len(result["email"]) == len(email), "Email count should match"
    for input_email, output_email in zip(email, result["email"]):
        assert input_email == output_email, f"Email should match (expected {input_email}, got {output_email})"

    assert len(result["phone"]) == len(phone), "Phone count should match"
    for input_phone, output_phone in zip(phone, result["phone"]):
        assert input_phone == output_phone, f"Phone should match (expected {input_phone}, got {output_phone})"


@pytest.mark.parametrize(
    "name",
    [
        "John Doe",
        "Alice-Wonderland",
        "123456",
        "!@#$%^",
        "A",
        "X" * 50,
    ],
    ids=["normal", "compound", "digits", "special-chars", "one-char", "long-name"]
)
def test_create_person_name_only(pd_client, created_person_ids, name):
    """Checks person creation with different kinds of 'name' values only."""
    result = pd_client.create_person(name=name)
    person_id = result["id"]
    created_person_ids.append(person_id)

    assert result["name"] == name, "Person name mismatch"

    fetched = pd_client.get_person(person_id)
    assert fetched["name"] == name, "Fetched person name mismatch"


@pytest.mark.parametrize(
    "phone,label",
    [
        ("111-222-3333", "work"),
        ("999888777", "home"),
        ("+1 (555) 123", "mobile"),
        ("54321", "other"),
    ],
    ids=["work", "home", "mobile", "other"]
)
def test_create_person_single_phone(pd_client, created_person_ids, phone, label):
    """Creates a person with a single phone number under different labels."""
    phone_data = [{"label": label, "value": phone, "primary": True}]
    result = pd_client.create_person(name="Test Phone", phone=phone_data)
    person_id = result["id"]
    created_person_ids.append(person_id)

    assert result["phone"] == phone_data, "Phone mismatch"

    fetched = pd_client.get_person(person_id)
    assert fetched["phone"] == phone_data, "Fetched phone mismatch"


@pytest.mark.parametrize(
    "phones",
    [
        (
                [
                    {"label": "work", "value": "111-111", "primary": True},
                    {"label": "home", "value": "222-222", "primary": False},
                ]
        ),
        (
                [
                    {"label": "mobile", "value": "333-333", "primary": True},
                    {"label": "other", "value": "444-444", "primary": False},
                ]
        ),
    ],
    ids=["work-home", "mobile-other"]
)
def test_create_person_multiple_phones(pd_client, created_person_ids, phones):
    """Creates a person with 2 phone entries (different labels)."""
    result = pd_client.create_person(name="MultiPhoneUser", phone=phones)
    person_id = result["id"]
    created_person_ids.append(person_id)

    assert result["phone"] == phones, "Phone list mismatch"

    fetched = pd_client.get_person(person_id)
    assert fetched["phone"] == phones, "Fetched phone list mismatch"


@pytest.mark.parametrize(
    "email,label",
    [
        ("john.doe@example.com", "work"),
        ("jane@home.net", "home"),
        ("somebody@somewhere", "other"),
        ("no-at-symbol.com", "other"),
    ],
    ids=["valid-work", "valid-home", "missing-tld", "no-at-symbol"]
)
def test_create_person_single_email(pd_client, created_person_ids, email, label):
    """Creates a person with a single email address under different labels."""
    email_data = [{"label": label, "value": email, "primary": True}]
    result = pd_client.create_person(name="Test Email", email=email_data)
    person_id = result["id"]
    created_person_ids.append(person_id)

    assert result["email"] == email_data, "Email mismatch"

    fetched = pd_client.get_person(person_id)
    assert fetched["email"] == email_data, "Fetched email mismatch"


@pytest.mark.parametrize(
    "labels",
    [
        [14],
        [14, 16],
    ],
    ids=["one-label", "two-labels"]
)
def test_create_person_multiple_labels(pd_client, created_person_ids, labels):
    """Creates a person with multiple 'labels'."""
    result = pd_client.create_person(name="MultiLabelUser", label_ids=labels)
    person_id = result["id"]
    created_person_ids.append(person_id)

    fetched_person = pd_client.get_person(person_id)
    assert fetched_person["label_ids"] == labels, f"Expected label_ids={labels}, got {fetched_person['label_ids']}"


@pytest.mark.parametrize(
    "with_org",
    [True, False],
    ids=["with-org", "without-org"]
)
def test_create_person_organization(pd_client, created_person_ids, created_org, with_org):
    """Creates a person with or without referencing an existing Organization."""
    org_id = created_org["id"] if with_org else None
    result = pd_client.create_person(name="UserWithOrWithoutOrg", org_id=org_id)
    person_id = result["id"]
    created_person_ids.append(person_id)

    if with_org:
        response_org_id = result["org_id"].get("value") if isinstance(result["org_id"], dict) else result["org_id"]
        assert response_org_id == org_id, f"Expected org_id={org_id}, but got {response_org_id}"
    else:
        assert result["org_id"] is None, "Should not have org_id when not provided"

    fetched = pd_client.get_person(person_id)
    if with_org:
        fetched_org_id = fetched["org_id"].get("value") if isinstance(fetched["org_id"], dict) else fetched["org_id"]
        assert fetched_org_id == org_id, f"Fetched org_id mismatch. Expected {org_id}, got {fetched_org_id}"
    else:
        assert fetched["org_id"] is None, "Fetched org_id should be None"


def test_create_person_existing_name(pd_client, created_person_ids, faker_instance):
    """Create a person with a name that already exists."""
    name = faker_instance.name()

    result1 = pd_client.create_person(name=name)
    created_person_ids.append(result1["id"])

    result2 = pd_client.create_person(name=name)
    created_person_ids.append(result2["id"])

    assert result1["name"] == name, "First person's name should match"
    assert result2["name"] == name, "Second person's name should match"

    assert result1["id"] != result2["id"], "IDs should be unique for each person"


def test_create_person_missing_name(pd_client, faker_instance):
    """Attempt to create a person with no name."""
    with pytest.raises(requests.exceptions.HTTPError):
        pd_client.create_person(
            name="",
            phone=faker_instance.phone_number(),
            email=faker_instance.email()
        )
