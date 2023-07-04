# airflow_supporter

airflow_supporter provide services to supporter to manage Apache Airflow

## Usage

1. Alert email on off DAG and turn on DAG automatically
    - Insert following example in your DAG
      ```python
      from airflow_supporter.dag.check_off_dag import create_check_off_dag
      create_check_off_dag()
      ```

    - Variable
      - enroll following Variable in your airflow
      - `check_off_dag_variable`
      ```
        {
          exclude_dag_list: list[str],  default empty list,
          automatically_turn_on: bool, default true,
          email: Optional[str]
        }
      ```

2. Restart failed DagRun
   ```python
    @dag(dag_id="restart_failed_dagrun_dag", schedule="* * * * *", is_paused_upon_creation=False, catchup=False,
        start_date=datetime(year=1970, month=1, day=1), )
    def restart_failed_dagrun_dag() -> None:
        restart_failed_dagrun_op.restart_failed_dagrun_op(rv=RestartFailedDagrunVariable())

    restart_failed_dagrun_dag()
   ```

3. Restart stucked Task
   ```python
     @dag(dag_id="clear_stucked_task_dag", schedule="* * * * *", is_paused_upon_creation=False, catchup=False,
         start_date=datetime(year=1970, month=1, day=1), )
     def clear_stucked_task_dag() -> None:
         restart_stucked_task_op.clear_stucked_task_op(rv=RestartStuckedTaskVariable())
   
     clear_stucked_task_dag()
   ```
