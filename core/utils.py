import ipaddress
import datetime
import os

def validate_ip(ip: str) -> bool:
    """Validates if the given string is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_timestamp() -> datetime:
    """Returns the current timestamp as a datetime object."""
    return datetime.datetime.now(datetime.timezone.utc)

def ensure_directory_exists(filepath: str) -> None:
    """Ensures the directory for the given filepath exists."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
