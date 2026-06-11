from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class Visibility(str, Enum):
    VISIBILITY_UNSPECIFIED = "VISIBILITY_UNSPECIFIED"
    PRIVATE = "PRIVATE"
    PROTECTED = "PROTECTED"
    PUBLIC = "PUBLIC"

class State(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    NORMAL = "NORMAL"
    ARCHIVED = "ARCHIVED"

class Memo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )

    name: str
    state: State = State.NORMAL
    creator: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None
    content: str
    visibility: Visibility = Visibility.PRIVATE
    pinned: bool = False
    tags: List[str] = Field(default_factory=list)

    @property
    def memo_id(self) -> str:
        """Extract the numeric ID or UUID from the resource name 'memos/{id}'."""
        return self.name.split("/")[-1]

class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )

    name: str
    role: str
    username: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    description: Optional[str] = None
    state: Optional[State] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None

class ListMemosResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    memos: List[Memo] = Field(default_factory=list)
    next_page_token: str = ""
