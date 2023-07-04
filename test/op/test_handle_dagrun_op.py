from __future__ import annotations

from typing import TYPE_CHECKING

from airflow.models import DagRun
from airflow.models import TaskInstance
from airflow.utils.session import provide_session
from airflow.utils.state import DagRunState
from airflow.utils.state import State

from airflow_supporter.model import RestartFailedDagrunVariable
from airflow_supporter.model import RestartStuckedTaskVariable
from airflow_supporter.service import handle_dag_op


if TYPE_CHECKING:
    from collections.abc import Iterator


def test_restart_failed_dagrun_func(create_data):
    @provide_session
    def _t(session):
        handle_dag_op.restart_failed_dagrun_func(
            rv=RestartFailedDagrunVariable(  # type: ignore[call-arg]
                restart_after_second=0,
            )
        )

        dagrun_list: Iterator[DagRun] = session.query(DagRun).all()
        for dr in dagrun_list:
            if dr.run_id in ["r1"]:
                assert dr.state == DagRunState.QUEUED
            if dr.run_id in ["r2"]:
                assert dr.state == DagRunState.SUCCESS

    _t()  # type: ignore[call-arg]


def test_restart_stucked_task_func(create_data):
    @provide_session
    def _t(session):
        handle_dag_op.restart_stucked_task_func(
            rv=RestartStuckedTaskVariable(restart_after_second=0, )
        )

        ti_list: Iterator[TaskInstance] = session.query(TaskInstance).all()
        for ti in ti_list:
            if ti.task_id in ["t1"]:
                assert ti.state == State.NONE
            if ti.task_id in ["t2"]:
                assert ti.state == DagRunState.FAILED

    _t()  # type: ignore[call-arg]
