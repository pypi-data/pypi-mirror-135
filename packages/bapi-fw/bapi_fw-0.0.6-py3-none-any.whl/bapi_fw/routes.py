
from typing import Callable, Any, Optional
from pydantic import BaseModel


class Route(BaseModel):
    path: str
    endpoint: Callable
    method: str
    # name: Optional[str]
    status_code: int = 200

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        # if data['name'] is None:
        #     self.name = self.endpoint.__name__
        # else:
        #     self.name = data['name']
