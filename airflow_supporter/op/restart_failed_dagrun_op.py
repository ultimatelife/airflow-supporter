from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from airflow.decorators import task

from airflow_supporter.service import handle_dag_op


if TYPE_CHECKING:
    from airflow_supporter.model import RestartFailedDagrunVariable

logger = logging.getLogger(__name__)


@task
def restart_failed_dagrun_op(rv: RestartFailedDagrunVariable) -> None:
    handle_dag_op.restart_failed_dagrun_func(rv)
