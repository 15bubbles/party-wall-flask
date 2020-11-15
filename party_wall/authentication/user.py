from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class User:
    id: str
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    authenticated: bool = False
    superuser: bool = False

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __ne__(self, other) -> bool:
        return self.id != other.id

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_authenticated(self) -> bool:
        return self.authenticated

    def get_id(self):
        return str(self.id)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NewUser:
    username: str
    password: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
