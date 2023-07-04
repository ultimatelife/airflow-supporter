from __future__ import annotations

import pydantic


class RestartFailedDagrunVariable(pydantic.BaseModel):
    """ """

    restart_after_second: int = 300


class RestartStuckedTaskVariable(pydantic.BaseModel):
    """ """

    restart_after_second: int = 300
