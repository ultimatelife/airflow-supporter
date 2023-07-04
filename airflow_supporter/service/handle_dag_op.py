from __future__ import annotations

import logging

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import TYPE_CHECKING

from airflow.models import DagRun
from airflow.models import TaskInstance
from airflow.utils.session import provide_session
from airflow.utils.state import DagRunState
from airflow.utils.state import State


if TYPE_CHECKING:
    from collections.abc import Iterator

    from airflow_supporter.model import RestartFailedDagrunVariable
    from airflow_supporter.model import RestartStuckedTaskVariable

logger = logging.getLogger(__name__)


@provide_session
def restart_failed_dagrun_func(rv: RestartFailedDagrunVariable,  # type: ignore[no-untyped-def]
                               session=None) -> None:
    ft = [
        DagRun.state.in_([DagRunState.FAILED]),
        DagRun.start_date
        < datetime.now(timezone.utc) - timedelta(seconds=rv.restart_after_second),
    ]

    dr_list: Iterator[DagRun] = session.query(DagRun).filter(*ft).all()
    logger.info(f"dr_list: {dr_list}")

    for dr in dr_list:
        dr.state = DagRunState.QUEUED
        session.merge(dr)

    logger.info("Done")


@provide_session
def restart_stucked_task_func(rv: RestartStuckedTaskVariable,  # type: ignore[no-untyped-def]
                              session=None) -> None:
    ft = [
        TaskInstance.state == State.QUEUED,
        TaskInstance.queued_dttm
        < datetime.now(timezone.utc) - timedelta(minutes=rv.restart_after_second),
    ]

    tis: Iterator[TaskInstance] = session.query(TaskInstance).filter(*ft).all()
    logger.info(f"tis: {tis}")

    for ti in tis:
        ti.try_number = ti.next_try_number
        ti.state = State.NONE
        session.merge(ti)

    logger.info("Done")
