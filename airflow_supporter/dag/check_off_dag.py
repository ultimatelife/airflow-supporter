from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from airflow.decorators import task
from airflow.operators.email import EmailOperator

from airflow_supporter.service import check_off_dag_op


if TYPE_CHECKING:
    from airflow import DAG

    from airflow_supporter.model import CheckOffDagVariable

logger = logging.getLogger(__name__)


def create_check_off_dag(codv: CheckOffDagVariable, dag: DAG) -> None:
    """
    This will create DAG named 'check_off_dag'


    Returns:
        None
    """

    with dag:
        @task
        def get_off_dag_list_op(exclude_dag_list: list[str]) -> list[str]:
            return check_off_dag_op.get_off_dag_list_func(exclude_dag_list)

        @task
        def turn_on_dag_op(dag_list: list[str]) -> None:
            check_off_dag_op.turn_of_dag_func(dag_list)

        off_dag_list_op = get_off_dag_list_op(codv.exclude_dag_list)

        if codv.email:
            EmailOperator(
                task_id="alert_off_dag_list_op",
                to=codv.email,
                subject="alert check_off_dag",
                html_content=",".join(off_dag_list_op),
            )

        turn_on_dag_op(off_dag_list_op)
