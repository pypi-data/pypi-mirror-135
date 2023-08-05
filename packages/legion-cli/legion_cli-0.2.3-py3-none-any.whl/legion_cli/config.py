from typing import Optional

from pydantic.dataclasses import dataclass


class Strict:
    extra = "forbid"


@dataclass(config=Strict)
class AppConfig():
    user_name: str
    hello_suffix: Optional[str] = None
