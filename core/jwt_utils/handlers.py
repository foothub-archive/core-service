def jwt_get_uuid_from_payload_handler(payload: dict) -> str:
    """
    Take the uuid, "Profile" table unique key
    """
    return payload['uuid']
