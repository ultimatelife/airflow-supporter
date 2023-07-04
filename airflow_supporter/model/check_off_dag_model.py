from __future__ import annotations

import pydantic


class CheckOffDagVariable(pydantic.BaseModel):
    exclude_dag_list: list[str] = []
    automatically_turn_on: bool = True
    email: str | None = None
