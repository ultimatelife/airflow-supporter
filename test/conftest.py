from __future__ import annotations

import pendulum
import pytest

from airflow.models import BaseOperator
from airflow.models import DagModel
from airflow.models import DagRun
from airflow.models import TaskInstance
from airflow.utils.session import provide_session
from airflow.utils.state import DagRunState
from airflow.utils.state import State
from airflow.utils.types import DagRunType
from sqlalchemy import func


@pytest.fixture(scope="session")
def create_data():
    @provide_session
    def _t(session):
        # insert Dag data
        session.query(DagModel).delete()
        d1 = DagModel(
            dag_id="d1",
            is_paused=0,
            is_subdag=0,
            is_active=0,
            last_parsed_time=func.now(),
            last_pickled=None,
            last_expired=None,
            scheduler_lock=None,
            pickle_id=None,
            fileloc=(
                "/home1/irteamsu/deploy/nfas-batch-airflow/dags/airflow-db-cleanup.py"
            ),
            owners="operations",
            description=None,
            default_view="grid",
            schedule_interval='"@daily"',
            root_dag_id=None,
            next_dagrun=func.now(),
            next_dagrun_create_after=func.now(),
            max_active_tasks=16,
            has_task_concurrency_limits=0,
            max_active_runs=16,
            next_dagrun_data_interval_start=func.now(),
            next_dagrun_data_interval_end=func.now(),
            has_import_errors=0,
            timetable_description="At 00:00",
            processor_subdir="/home1/irteamsu/deploy/nfas-batch-airflow/dags",
        )
        d2 = DagModel(
            dag_id="d2",
            is_paused=1,
            is_subdag=0,
            is_active=0,
            last_parsed_time=func.now(),
            last_pickled=None,
            last_expired=None,
            scheduler_lock=None,
            pickle_id=None,
            fileloc=(
                "/home1/irteamsu/deploy/nfas-batch-airflow/dags/airflow-db-cleanup.py"
            ),
            owners="operations",
            description=None,
            default_view="grid",
            schedule_interval='"@daily"',
            root_dag_id=None,
            next_dagrun=func.now(),
            next_dagrun_create_after=func.now(),
            max_active_tasks=16,
            has_task_concurrency_limits=0,
            max_active_runs=16,
            next_dagrun_data_interval_start=func.now(),
            next_dagrun_data_interval_end=func.now(),
            has_import_errors=0,
            timetable_description="At 00:00",
            processor_subdir="/home1/irteamsu/deploy/nfas-batch-airflow/dags",
        )
        d3 = DagModel(
            dag_id="d3",
            is_paused=1,
            is_subdag=0,
            is_active=0,
            last_parsed_time=func.now(),
            last_pickled=None,
            last_expired=None,
            scheduler_lock=None,
            pickle_id=None,
            fileloc=(
                "/home1/irteamsu/deploy/nfas-batch-airflow/dags/airflow-db-cleanup.py"
            ),
            owners="operations",
            description=None,
            default_view="grid",
            schedule_interval='"@daily"',
            root_dag_id=None,
            next_dagrun=func.now(),
            next_dagrun_create_after=func.now(),
            max_active_tasks=16,
            has_task_concurrency_limits=0,
            max_active_runs=16,
            next_dagrun_data_interval_start=func.now(),
            next_dagrun_data_interval_end=func.now(),
            has_import_errors=0,
            timetable_description="At 00:00",
            processor_subdir="/home1/irteamsu/deploy/nfas-batch-airflow/dags",
        )

        session.add(d1)
        session.add(d2)
        session.add(d3)
        session.commit()

        # insert DagRun data
        session.query(DagRun).filter(DagRun.run_id.in_(["r1", "r2"])).delete()

        dr1 = DagRun(
            dag_id="d1",
            run_id="r1",
            queued_at=func.now(),
            execution_date=func.now(),
            start_date=func.now(),
            run_type=DagRunType.SCHEDULED,
            state=DagRunState.FAILED,
        )
        dr2 = DagRun(
            dag_id="d2",
            run_id="r2",
            queued_at=func.now(),
            execution_date=func.now(),
            start_date=func.now(),
            run_type=DagRunType.SCHEDULED,
            state=DagRunState.SUCCESS,
        )
        session.add(dr1)
        session.add(dr2)
        session.commit()

        # insert DagRun data
        session.query(TaskInstance).filter(
            TaskInstance.task_id.in_(["t1", "t2"])
        ).delete()

        t1 = TaskInstance(
            task=BaseOperator(task_id="t1"),
            execution_date=pendulum.now(),
            run_id="r1",
            state=State.QUEUED,
        )
        t1.task_id = "t1"
        t1.dag_id = "d1"
        t1.start_date = pendulum.now()
        t1.end_date = pendulum.now()
        t1.duration = 2
        t1.state = State.QUEUED
        t1.try_number = 1
        t1.hostname = "h1"
        t1.unixname = "u1"
        t1.job_id = 1
        t1.pool = "default_pool"
        t1.queue = "default"
        t1.priority_weight = 9
        t1.operator = "PythonOperator"
        t1.queued_dttm = pendulum.now()
        t1.pid = 1
        t1.max_tries = 5
        t1.executor_config = None
        t1.pool_slots = 1
        t1.queued_by_job_id = 1
        t1.external_executor_id = None
        t1.trigger_id = None
        t1.next_method = None
        t1.next_kwargs = None

        t2 = TaskInstance(
            task=BaseOperator(task_id="t2"),
            execution_date=pendulum.now(),
            run_id="r2",
            state=State.FAILED,
        )
        t2.task_id = "t2"
        t2.dag_id = "d2"
        t2.start_date = pendulum.now()
        t2.end_date = pendulum.now()
        t2.duration = 2
        t2.state = State.FAILED
        t2.try_number = 1
        t2.hostname = "h2"
        t2.unixname = "u2"
        t2.job_id = 2
        t2.pool = "default_pool"
        t2.queue = "default"
        t2.priority_weight = 9
        t2.operator = "PythonOperator"
        t2.queued_dttm = pendulum.now()
        t2.pid = 2
        t2.max_tries = 5
        t2.executor_config = None
        t2.pool_slots = 1
        t2.queued_by_job_id = 1
        t2.external_executor_id = None
        t2.trigger_id = None
        t2.next_method = None
        t2.next_kwargs = None

        session.add(t1)
        session.add(t2)
        session.commit()
