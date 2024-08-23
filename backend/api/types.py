from typing import TypedDict, Optional
from globalTypes import RegistrationType


class RegistrationPayload(TypedDict):
    name: str
    companyName: Optional[str]
    age: str
    email: str
    password: str
    type: RegistrationType


class ConfirmCodePayload(TypedDict):
    id: str
    email: str
