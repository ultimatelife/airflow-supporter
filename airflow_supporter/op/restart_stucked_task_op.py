from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from airflow.decorators import task

from airflow_supporter.service import handle_dag_op


if TYPE_CHECKING:
    from airflow_supporter.model import RestartStuckedTaskVariable

logger = logging.getLogger(__name__)


@task
def clear_stucked_task_op(rv: RestartStuckedTaskVariable) -> None:
    handle_dag_op.restart_stucked_task_func(rv)
