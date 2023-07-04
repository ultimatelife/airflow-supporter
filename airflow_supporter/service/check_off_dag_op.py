from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from airflow.models import DagModel
from airflow.utils.session import provide_session

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)


@provide_session
def _get_off_dag_list(session=None) -> list[str]:  # type: ignore[no-untyped-def]
    dag_list: Iterator[DagModel] = (
        session.query(DagModel)
            .filter((DagModel.is_paused == 1) | (DagModel.is_active == 0))
            .all()
    )
    dag_name_list: list[str] = [str(d.dag_id) for d in dag_list]

    logger.info(f"dag_name_list: {dag_name_list}")
    return dag_name_list


def get_off_dag_list_func(exclude_dag_list: list[str]) -> list[str]:
    logger.info(f"exclude_dag_list: {exclude_dag_list}")
    result = [d for d in _get_off_dag_list() if d not in exclude_dag_list]
    logger.info(f"result: {result}")
    return result


@provide_session
def turn_of_dag_func(dag_list: list[str], session=None):  # type: ignore[no-untyped-def]
    session.query(DagModel).filter(DagModel.dag_id.in_(dag_list)).update(
        {"is_paused": False, "is_active": True}
    )
    session.commit()
