"""Internal validation helpers shared by domain models."""

from datetime import datetime


def require_non_empty(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")
    return value


def require_aware_datetime(value: object, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include timezone information")
    return value


def parse_datetime(value: object, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be an ISO 8601 string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must be a valid ISO 8601 datetime") from error
    return require_aware_datetime(parsed, field_name)


def require_non_negative_int(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must not be negative")
    return value
