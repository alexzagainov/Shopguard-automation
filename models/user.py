import uuid
from dataclasses import dataclass, field
from typing import Optional


def unique_email() -> str:
    return f"alex_{uuid.uuid4().hex[:10]}@test.com"


@dataclass
class User:
    name: str = "Alex"
    # every User gets a new email, because the site rejects emails that are already registered
    email: str = field(default_factory=unique_email)
    password: str = "1234567"
    title: str = "Mr"
    day_of_birth: str = "2"
    month_of_birth: str = "3"
    year_of_birth: str = "2000"
    newsletter: bool = False
    special_offers: bool = False
    # None = leave the field empty (for negative tests)
    first_name: Optional[str] = "Alex"
    last_name: Optional[str] = "Zaga"
    company: Optional[str] = "ZAGAQA"
    address: Optional[str] = "NITZAHON B"
    address2: Optional[str] = ""
    country: str = "Israel"
    state: Optional[str] = "Israel"
    city: Optional[str] = "Netanya"
    zipcode: Optional[str] = "4237676"
    mobile_number: Optional[str] = "0521234567"