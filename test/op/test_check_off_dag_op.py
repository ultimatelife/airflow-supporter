from __future__ import annotations

from typing import TYPE_CHECKING

from airflow.models import DagModel
from airflow.utils.session import provide_session

from airflow_supporter.service import check_off_dag_op


if TYPE_CHECKING:
    from collections.abc import Iterator


def test_turn_of_dag_func(create_data):
    @provide_session
    def _t(session):
        check_off_dag_op.turn_of_dag_func(
            check_off_dag_op.get_off_dag_list_func(["d3"])
        )

        dag_list: Iterator[DagModel] = session.query(DagModel).all()

        for dm in dag_list:
            print(
                f"dm.dag_id: {dm.dag_id} dm.is_active: {dm.is_active} dm.is_paused:"
                f" {dm.is_paused}"
            )
            if dm.dag_id in ["d1", "d2"]:
                assert dm.is_active
                assert not dm.is_paused
            else:
                assert not dm.is_active
                assert dm.is_paused

    _t()
